#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import contextvars
from functools import wraps
import inspect
import os
import pathlib
from typing import Any, Callable, cast, Dict, Optional, Union

import yaml

from datarobot.analytics import get_stack_trace
from datarobot.context import Context as DRContext
from datarobot.context import _ContextGlobals

_config_initialized = contextvars.ContextVar("config_initialized", default=False)
_token = contextvars.ContextVar("token", default="")
_endpoint = contextvars.ContextVar("endpoint", default="")
_pred_server_id = contextvars.ContextVar("pred_server_id", default="")
_rest_poll_interval = contextvars.ContextVar("rest_poll_interval", default=3.0)
_max_wait = contextvars.ContextVar("max_wait", default=24 * 60 * 60)
_upload_file_type = contextvars.ContextVar("upload_file_type", default="csv")
_theme = contextvars.ContextVar("theme", default="dark")
# https://datarobot.atlassian.net/browse/RAPTOR-10125
_disable_chunked_uploads = contextvars.ContextVar(
    "disable_chunked_uploads",
    default=(os.environ.get("DATAROBOT_ENDPOINT", "") == "http://datarobot-nginx/api/v2"),
)


_concurrency_poll_interval = contextvars.ContextVar("concurrency_poll_interval", default=0.2)

_max_dr_ingest = contextvars.ContextVar("max_dr_ingest", default=5 * (10**9))

ScalerType = Union[str, int, float, bool]
ContextScalarTypes = Union[
    contextvars.ContextVar[str],
    contextvars.ContextVar[int],
    contextvars.ContextVar[float],
    contextvars.ContextVar[bool],
]


_global_context: Dict[str, ScalerType] = {}


def env_to_bool(env_value: ScalerType) -> bool:
    """
    A helper function to convert environment variable strings or ints into bools
    """
    return env_value not in ["no", "No", "0", "false", "False"]


# Context variable for the public entry point (function name) into threaded drx work
drx_task_entry_point: contextvars.ContextVar[str] = contextvars.ContextVar("drx_task_entry_point")


def get_task_entry_point() -> str:
    """Retrieve the public entry point for threaded drx work."""
    try:
        return drx_task_entry_point.get()
    except LookupError:
        pass

    depth = 2  # caller -> create_task_new_thread() -> get_task_entry_point()
    stack = inspect.stack()
    return get_stack_trace(stack[depth:])


def is_notebook_env() -> bool:
    """Detect if this is an interactive, ipython-based notebook."""
    try:
        from IPython import get_ipython, InteractiveShell  # pylint: disable=import-outside-toplevel

        ip: Optional[InteractiveShell] = get_ipython()  # type: ignore[no-untyped-call]
        if ip is not None and ip.has_trait("kernel"):
            return True
    except ImportError:
        pass
    return False


_force_task_blocking = contextvars.ContextVar("force_task_blocking", default=not is_notebook_env())


def set_global_context(drx_context: Dict[str, str | int | float | bool]) -> None:
    """Updates the global context to match the current context that was invoked by the user
    (via environment variables or other measn). This was developed to help
    in runtimes that clear contextvars inadvertently.

    See https://github.com/ipython/ipython/issues/11565 for more details

    Parameters
    ----------
    drx_context : Dict representing the context variables unpacked and ready to go.
    """
    global _global_context  # pylint: disable=W0603
    _global_context = drx_context


def drx_context_getter(
    var: ContextScalarTypes,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """This decorator handles situations where contextvars are inadvertently cleared
    this occurs in some kernels such as Google Colab where context is not maintained
    across cells.

    Each property getter method on drx.Context will call `.get` on it's contextvar.
    This decorator will first check to see if that contextvar has been set and if not will try and return a value
    from `_global_context`. The order of operations is as follows:

    1. First, check if the contextvar is set. If set, return that value.
    2. If not set, check for value in global context dictionary.
    3. if no value is present, return the contextvar default.
    """

    def unpack_getter(func: Callable[..., ScalerType]) -> Callable[..., ScalerType]:
        @wraps(func)
        def wrapper(
            _object: Context,
        ) -> ScalerType:
            if var not in contextvars.copy_context():  # 1. check if the contextvar is set
                # 2. check if the var exists in the global context dictionary.
                return _global_context.get(
                    var.name, func(_object)
                )  # noqa: E501 3. if no value is present, return the contextvar default.
            else:
                return (
                    var.get()
                )  # fallback to the variable if this variable has never been added to global context.

        return wrapper

    return unpack_getter


class ConfigReader:
    """Read configuration parameters from DataRobot YAML and environment variables
    with the latter taking precedence over the former.

    Parameters
    ----------
    config_path : Union[pathlib.Path, str]
        Path to the yaml config file
    env : bool=True
        Whether to read environment variables
    global_context : bool=True
        Whether to use the stored global dictionary which helps in runtimes that destroy the context.
    """

    def __init__(
        self,
        config_path: Optional[Union[pathlib.Path, str]] = None,
        env: bool = True,
        global_context: bool = True,
    ):
        if isinstance(config_path, str):
            config_path = pathlib.Path(config_path)
        self.config_path = config_path
        self.env = env
        self.global_context = global_context

    def load_yaml(self) -> Dict[str, Any]:
        """Read DR config yaml if it exist."""
        try:
            with self.config_path.open(mode="rb") as f:  # type: ignore[union-attr]
                return cast(Dict[str, Any], yaml.load(f, Loader=yaml.Loader))
        except (OSError, yaml.YAMLError):
            return {}

    @staticmethod
    def load_env() -> Dict[str, ScalerType]:
        """Read environment variable config values if present."""
        env_config: Dict[str, ScalerType] = {}
        if "DATAROBOT_API_TOKEN" in os.environ:
            env_config["token"] = os.environ["DATAROBOT_API_TOKEN"]
        if "DATAROBOT_ENDPOINT" in os.environ:
            env_config["endpoint"] = os.environ["DATAROBOT_ENDPOINT"]
        if "DATAROBOT_PRED_SERVER_ID" in os.environ:
            env_config["pred_server_id"] = os.environ["DATAROBOT_PRED_SERVER_ID"]
        if "DATAROBOT_ENABLE_API_CONSUMER_TRACKING" in os.environ:
            env_config["enable_api_consumer_tracking"] = env_to_bool(
                os.environ["DATAROBOT_ENABLE_API_CONSUMER_TRACKING"]
            )
        if "DATAROBOT_TRACE_CONTEXT" in os.environ:
            env_config["trace_context"] = os.environ["DATAROBOT_TRACE_CONTEXT"]
        return env_config

    @staticmethod
    def load_global_context() -> Dict[str, ScalerType]:
        """Read global context config values if present."""
        env_config: Dict[str, ScalerType] = {}
        if "token" in _global_context:
            env_config["token"] = _global_context["token"]
        if "endpoint" in _global_context:
            env_config["endpoint"] = _global_context["endpoint"]
        if "pred_server_id" in _global_context:
            env_config["pred_server_id"] = _global_context["pred_server_id"]
        if "enable_api_consumer_tracking" in _global_context:
            env_config["enable_api_consumer_tracking"] = env_to_bool(
                _global_context["enable_api_consumer_tracking"]
            )
        if "trace_context" in _global_context:
            env_config["trace_context"] = _global_context["trace_context"]
        return env_config

    def read(self) -> Dict[str, Any]:
        """Dictionary of read parameters.
        Precedence: 1. Global Config, 2. environment 3. yaml just for the these five keys not the full dictionary
        """
        yaml_config = {}
        env_config = {}
        globals_config = {}
        if self.config_path:
            yaml_config = self.load_yaml()
        if self.env:
            env_config = self.load_env()
        if self.global_context:
            globals_config = self.load_global_context()

        return {**yaml_config, **env_config, **globals_config}


class Context:
    """
    Interface for initializing, accessing, and setting drx context variables.

    Parameters
    ----------
    token : str
        DataRobot API token
    endpoint : str
        DataRobot API endpoint
    pred_server_id : str
        Default prediction server id to use for deployments
    config_path : str
        Path to DataRobot configuration yaml file. If specified, values for token,
        endpoint, and pred_server_id in the yaml file will take precedence.

    Examples
    --------
    >>> import datarobotx as drx
    >>> drx.Context()  # show current configuration
    {'token': '***', 'endpoint': 'https://app.datarobot.com/api/v2', 'pred_server_id': '***'}
    >>> drx.Context(token='foo', endpoint='bar')  # update current configuration
    {'token': 'foo', 'endpoint': 'bar', 'pred_server_id': '***'}
    >>> c = drx.Context()
    >>> c.pred_server_id = 'foo_bar'  # alternative approach to update
    >>> drx.Context()
    {'token': 'foo', 'endpoint': 'bar', 'pred_server_id': 'foo_bar'}
    >>> drx.Context(config_path='my_path/my_config.yaml')  # update from file
    {'token': 'my_config_token', 'endpoint': 'my_config_endpoint', 'pred_server_id': 'my_config_pred_server_id'}
    """

    def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        getattr(self, "", None)  # trigger just-in-time defaults initialization (if needed)
        # Read from kwargs to allow user to explicitly reset params to None
        if "token" in kwargs:
            self.token = kwargs["token"]
        if "endpoint" in kwargs:
            self.endpoint = kwargs["endpoint"]
        if "pred_server_id" in kwargs:
            self.pred_server_id = kwargs["pred_server_id"]
        if "config_path" in kwargs:
            self._init_from_file(kwargs["config_path"])
        if "enable_api_consumer_tracking" in kwargs:
            DRContext.enable_api_consumer_tracking = kwargs["enable_api_consumer_tracking"]
        if "trace_context" in kwargs:
            DRContext.trace_context = kwargs["trace_context"]

    def __getattribute__(self, name: str) -> Any:
        """When an attribute is needed from the Context object, ensure that the context value has actually been set.
        If it is not set initialize context from file or environment using a ConfigReader. The ConfigReader will take
        into account precedence in loading variables:

        1. Global Config, 2. environment 3. yaml.

        Thus, a previously set value that was stored in global config will override
        an envrionment variable which will override a yaml file in the default location.

        This functionality is required for runtimes that don't maintain context (contextvars) throughout
        the lifecycle. We colloquially refer to these as "context killers". Thus by relying,
        on the global context dictionary, we account for cases when context is not maintained.

        See https://github.com/ipython/ipython/issues/11565 for more details
        """
        if not _config_initialized.get():
            _config_initialized.set(True)
            Context.__init__(
                self,
                **ConfigReader(
                    pathlib.Path("~/.config/datarobot/drconfig.yaml").expanduser().resolve()
                ).read(),
            )
        if name in ["enable_api_consumer_tracking", "trace_context"]:
            return DRContext.__getattribute__(name)
        return super().__getattribute__(name)

    def _init_from_file(self, config_path: pathlib.Path) -> None:
        """Update context from config file, env variables."""
        config = ConfigReader(config_path, env=False, global_context=False).read()
        self.token = config.get("token", self.token)
        self.endpoint = config.get("endpoint", self.endpoint)
        self.pred_server_id = config.get("pred_server_id", self.pred_server_id)

    def _update_and_set_global_context(self) -> None:
        """Copies the context object attributes into a global dictionary."""

        def unpack(
            v: str | int | float | bool | contextvars.ContextVar[str],
        ) -> str | int | float | bool:
            """Don't stick a context var into the dict. If it's a contextvar GET it first"""
            if isinstance(v, contextvars.ContextVar):
                return v.get()
            else:
                return v

        self.local_context = {  # pylint: disable=W0201
            k.name: unpack(v) for k, v in contextvars.copy_context().items()
        }
        set_global_context(self.local_context)

    @property
    @drx_context_getter(_token)
    def token(self) -> str:
        """DataRobot API token."""
        return _token.get()

    @token.setter
    def token(self, value: str) -> None:
        _token.set(value)
        self._update_and_set_global_context()

    @property
    @drx_context_getter(_endpoint)
    def endpoint(self) -> str:
        """DataRobot API endpoint."""
        return _endpoint.get()

    @endpoint.setter
    def endpoint(self, value: str) -> None:
        _endpoint.set(value)
        self._update_and_set_global_context()

    @property
    @drx_context_getter(_pred_server_id)
    def pred_server_id(self) -> str:
        """DataRobot prediction server id for deployments."""
        return _pred_server_id.get()

    @pred_server_id.setter
    def pred_server_id(self, value: str) -> None:
        _pred_server_id.set(value)
        self._update_and_set_global_context()

    @property
    def dr_context(self) -> _ContextGlobals:
        return DRContext

    @property
    @drx_context_getter(_rest_poll_interval)
    def _rest_poll_interval(self) -> float:
        """HTTP polling interval in seconds for DataRobot status."""
        return float(_rest_poll_interval.get())

    @_rest_poll_interval.setter
    def _rest_poll_interval(self, value: int | float) -> None:
        if isinstance(value, int):
            _rest_poll_interval.set(float(value))
        else:
            _rest_poll_interval.set(value)
        self._update_and_set_global_context()

    @property
    @drx_context_getter(_max_wait)
    def _max_wait(self) -> int:
        """Maximum polling duration before timeout in seconds."""
        return int(_max_wait.get())

    @_max_wait.setter
    def _max_wait(self, value: int) -> None:
        _max_wait.set(value)
        self._update_and_set_global_context()

    @property
    def _webui_base_url(self) -> str:
        """Base url for links to the DataRobot WebUI."""
        return str(self.endpoint.split("/api")[0])

    @property
    def _auth_header(self) -> Dict[str, str]:
        """DataRobot HTTP API headers for authentication."""
        return {"Authorization": "Bearer " + self.token}

    @property
    @drx_context_getter(_concurrency_poll_interval)
    def _concurrency_poll_interval(self) -> float:
        """drx local polling interval while awaiting long running operations."""
        return float(_concurrency_poll_interval.get())

    @property
    @drx_context_getter(_force_task_blocking)
    def _force_task_blocking(self) -> bool:
        """Force all drx tasks to block."""
        return bool(_force_task_blocking.get())

    @property
    @drx_context_getter(_max_dr_ingest)
    def _max_dr_ingest(self) -> int:
        """Maximum DR upload size in bytes."""
        return int(_max_dr_ingest.get())

    @_max_dr_ingest.setter
    def _max_dr_ingest(self, value: int) -> None:
        _max_dr_ingest.set(value)
        self._update_and_set_global_context()

    @property
    def _upload_file_type(self) -> str:
        """
        Default file type for drx upload.

        Valid types are 'csv' or 'parquet'
        """
        return _upload_file_type.get()

    @_upload_file_type.setter
    def _upload_file_type(self, value: str) -> None:
        _upload_file_type.set(value)

    @property
    @drx_context_getter(_theme)
    def theme(self) -> str:
        """Whether charts render in dark or light."""
        return str(_theme.get())

    @theme.setter
    def theme(self, value: str) -> None:
        _theme.set(value)
        self._update_and_set_global_context()

    @property
    @drx_context_getter(_disable_chunked_uploads)
    def disable_chunked_uploads(self) -> bool:
        """Whether to disable chunked uploads

        May be required in certain on-prem environments,
        but breaks upload progress bars"""
        return _disable_chunked_uploads.get()

    @disable_chunked_uploads.setter
    def disable_chunked_uploads(self, value: bool) -> None:
        _disable_chunked_uploads.set(value)
        self._update_and_set_global_context()

    def __repr__(self) -> str:
        d = {
            "token": self.token,
            "endpoint": self.endpoint,
            "pred_server_id": self.pred_server_id,
            "enable_api_consumer_tracking": self.dr_context.enable_api_consumer_tracking,
            "trace_context": self.dr_context.trace_context,
        }
        return d.__repr__()


context = Context()
