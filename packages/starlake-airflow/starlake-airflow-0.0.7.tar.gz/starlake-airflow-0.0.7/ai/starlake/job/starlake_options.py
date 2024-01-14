from __future__ import annotations

import json
import os

from ai.starlake.common import MissingEnvironmentVariable

class StarlakeOptions:
    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def get_context_var(cls, var_name: str, default_value: any=None, options: dict = None, **kwargs):
        """Get context variable."""
        if options and options.get(var_name):
            return options.get(var_name)
        elif default_value is not None:
            return default_value
        elif os.getenv(var_name) is not None:
            return os.getenv(var_name)
        else:
            raise MissingEnvironmentVariable(f"{var_name} does not exist")

    @classmethod
    def get_sl_env_vars(cls, options: dict) -> dict:
        """Get SL environment variables"""
        try:
            return json.loads(__class__.get_context_var(var_name="sl_env_var", options=options))
        except MissingEnvironmentVariable:
            return {}

    @classmethod
    def get_sl_root(cls, options: dict) -> str:
        """Get SL root"""
        return __class__.get_context_var(var_name='SL_ROOT', default_value='file://tmp', options=__class__.get_sl_env_vars(options))

    @classmethod
    def get_sl_datasets(cls, options: dict) -> str:
        """Get SL datasets"""
        return __class__.get_context_var(var_name='SL_DATASETS', default_value=f'{__class__.get_sl_root(options)}/datasets', options=__class__.get_sl_env_vars(options))