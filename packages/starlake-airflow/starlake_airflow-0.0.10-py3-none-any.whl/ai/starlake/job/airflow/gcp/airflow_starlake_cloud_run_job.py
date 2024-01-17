import os

from typing import Union

from ai.starlake.job import StarlakePreLoadStrategy, StarlakeSparkConfig

from ai.starlake.job.airflow import AirflowStarlakeJob

from airflow.models.baseoperator import BaseOperator

from airflow.operators.bash import BashOperator

from airflow.sensors.bash import BashSensor

from airflow.utils.task_group import TaskGroup

class AirflowStarlakeCloudRunJob(AirflowStarlakeJob):
    """Airflow Starlake Cloud Run Job."""
    def __init__(self, pre_load_strategy: Union[StarlakePreLoadStrategy, str, None]=None, project_id: str=None, cloud_run_job_name: str=None, cloud_run_job_region: str=None, options: dict=None, cloud_run_async:bool=None, retry_on_failure: bool=None, separator:str = ' ', **kwargs):
        super().__init__(pre_load_strategy=pre_load_strategy, options=options, **kwargs)
        self.project_id = __class__.get_context_var(var_name='cloud_run_project_id', default_value=os.getenv("GCP_PROJECT"), options=self.options) if not project_id else project_id
        self.cloud_run_job_name = __class__.get_context_var(var_name='cloud_run_job_name', options=self.options) if not cloud_run_job_name else cloud_run_job_name
        self.cloud_run_job_region = __class__.get_context_var('cloud_run_job_region', "europe-west1", self.options) if not cloud_run_job_region else cloud_run_job_region
        self.cloud_run_async = __class__.get_context_var(var_name='cloud_run_async', default_value="True", options=self.options).lower == "true" if not cloud_run_async else cloud_run_async
        self.separator = separator if separator != ',' else ' '
        self.update_env_vars = self.separator.join([(f"--update-env-vars \"^{self.separator}^" if i == 0 else "") + f"{key}={value}" for i, (key, value) in enumerate(self.sl_env_vars.items())]) + "\""
        self.retry_on_failure = __class__.get_context_var("retry_on_failure", "False", self.options).lower() == 'true' if retry_on_failure is None else retry_on_failure

    def __job_with_completion_sensors__(self, task_id: str, command: str, spark_config: StarlakeSparkConfig=None, **kwargs) -> TaskGroup:
        kwargs.update({'pool': kwargs.get('pool', self.pool)})
        with TaskGroup(group_id=f'{task_id}_wait') as task_completion_sensors:
            # asynchronous job
            job_task = BashOperator(
                task_id=task_id,
                bash_command=(
                    f"gcloud beta run jobs execute {self.cloud_run_job_name} "
                    f"--args \"{command}\" "
                    f"{self.update_env_vars} "
                    f"--async --region {self.cloud_run_job_region} --project {self.project_id} --format='get(metadata.name)'" #--task-timeout 300 
                ),
                do_xcom_push=True,
                **kwargs
            )
            # check job completion
            check_completion_id = task_id + '_check_completion'
            completion_sensor = CloudRunJobCompletionSensor(
                task_id=check_completion_id,
                project_id=self.project_id,
                cloud_run_job_region=self.cloud_run_job_region,
                source_task_id=job_task.task_id,
                retry_exit_code=1 if self.retry_on_failure else None,
                **kwargs
            )
            if self.retry_on_failure:
                job_task >> completion_sensor
            else:
                # check job status
                get_completion_status_id = task_id + '_get_completion_status'
                job_status = CloudRunJobCheckStatusOperator(
                    task_id=get_completion_status_id,
                    project_id=self.project_id,
                    cloud_run_job_region=self.cloud_run_job_region,
                    source_task_id=job_task.task_id,
                    **kwargs
                )
                job_task >> completion_sensor >> job_status
        return task_completion_sensors

    def sl_job(self, task_id: str, arguments: list, spark_config: StarlakeSparkConfig=None, **kwargs) -> BaseOperator:
        """Overrides AirflowStarlakeJob.sl_job()"""
        command = f'^{self.separator}^' + self.separator.join(arguments)
        if self.cloud_run_async:
            return self.__job_with_completion_sensors__(task_id=task_id, command=command, spark_config=spark_config, **kwargs)
        else:
            # synchronous job
            return BashOperator(
                task_id=task_id,
                bash_command=(
                    f"gcloud beta run jobs execute {self.cloud_run_job_name} "
                    f"--args \"{command}\" "
                    f"{self.update_env_vars} "
                    f"--wait --region {self.cloud_run_job_region} --project {self.project_id} --format='get(metadata.name)'" #--task-timeout 300 
                ),
                do_xcom_push=True,
                **kwargs
            )

class CloudRunJobCompletionSensor(BashSensor):
    '''
    This sensor checks the completion of a cloud run job.
    '''
    def __init__(self, *, project_id: str, cloud_run_job_region: str, source_task_id: str, retry_exit_code: int=None, **kwargs) -> None:
        if retry_exit_code:
            super().__init__(
                bash_command=(f"value=`gcloud beta run jobs executions describe {{{{task_instance.xcom_pull(key=None, task_ids='{source_task_id}')}}}}  --region {cloud_run_job_region} --project {project_id} --format='value(status.failedCount, status.cancelledCounts)' | sed 's/[[:blank:]]//g'`; test -z \"$value\""),
                mode="reschedule",
                retries=3, #the number of retries that should be performed before failing the task to avoid infinite loops
                retry_exit_code=retry_exit_code, #available in 2.6. Implies to combine this sensor and the bottom operator
                **kwargs
            )
        else:
            super().__init__(
                bash_command=(f"value=`gcloud beta run jobs executions describe {{{{task_instance.xcom_pull(key=None, task_ids='{source_task_id}')}}}}  --region {cloud_run_job_region} --project {project_id} --format='value(status.completionTime, status.cancelledCounts)' | sed 's/[[:blank:]]//g'`; test -n \"$value\""),
                mode="reschedule",
                #retry_exit_code=1, #available in 2.6. Implies to combine this sensor and the bottom operator
                **kwargs
            )

class CloudRunJobCheckStatusOperator(BashOperator):
    '''
    This operator checks the status of a cloud run job and fails if it is not successful.
    '''
    def __init__(self, *, project_id: str, cloud_run_job_region: str, source_task_id: str, **kwargs) -> None:
        super().__init__(
            bash_command=(f"value=`gcloud beta run jobs executions describe {{{{task_instance.xcom_pull(key=None, task_ids='{source_task_id}')}}}} --region {cloud_run_job_region} --project {project_id} --format='value(status.failedCount, status.cancelledCounts)' | sed 's/[[:blank:]]//g'`; test -z \"$value\""),
            **kwargs
        )
