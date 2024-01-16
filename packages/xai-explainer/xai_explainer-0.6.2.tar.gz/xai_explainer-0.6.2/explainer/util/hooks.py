import abc
from contextlib import ContextDecorator
from copy import deepcopy
import enum
import re
from typing import Any, List, Optional


class WriteLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    BASIC = 2
    NONE = 3


class _LazyCopy:
    """
    Wrapper class that allows for lazy deep copying of data. This is useful for callbacks that only want to copy the data if it is actually used.

    Args:
        data: The data to wrap. If data is already a _LazyDeepCopy, it is unwrapped.
    """

    def __init__(self, data: Any):
        self._data = (
            data if not isinstance(data, _LazyCopy) else data.data
        )  # unwrap if data is already a _LazyDeepCopy

    @property
    def data(self) -> Any:
        return deepcopy(self._data)


class Hook:
    """
    Base class for callbacks.

    Args:
        level (Optional[CallbackLevel]): The level of the callback. Defaults to CallbackLevel.NONE.

    Raises:
        TypeError: If level is not of type CallbackLevel.
        ValueError: If level is not a valid CallbackLevel.
    """

    def __init__(self, level: Optional[WriteLevel] = None):
        self.level = level
        self._prefixes = []

    @property
    def level(self) -> WriteLevel:
        return self._level

    @level.setter
    def level(self, level: Optional[WriteLevel]):
        level = WriteLevel(level) if level is not None else WriteLevel.NONE
        if not isinstance(level, WriteLevel):
            raise TypeError(f"level must be of type {WriteLevel}, not {type(level)}")
        self._level = level

    @property
    def prefix(self) -> str:
        prefix_builder = ""
        for idx, _prefix in enumerate(self._prefixes):
            prefix_builder += _prefix
            prefix_builder += "/" if idx != len(self._prefixes) - 1 else ""

        return prefix_builder

    @staticmethod
    def _check_url(url: str):
        if not isinstance(url, str):
            raise TypeError(f"prefix must be of type str, not {type(url)}")
        if len(url) == 0:
            raise ValueError("prefix must not be empty")

        ALLOWED_CHARS = r"[a-zA-Z0-9_+-,&%\[\]=\(\)\.]"
        target_regex = r"^{}+(/{}+)*/?$".format(ALLOWED_CHARS, ALLOWED_CHARS)
        target_regex = re.compile(target_regex)

        if not target_regex.match(url):
            allowed_chars = "_+-,[]=()."
            expected_format = "identifier/identifier/.../identifier"
            raise ValueError(
                f'Invalid URL: "{url}". Only URLs in the format "{expected_format}" are allowed, '
                f"where 'identifier' is an alphanumeric string with the additional characters: \"{allowed_chars}\". "
                f"Examples: 'some_id', 'id/', 'id1/id2'."
            )

    @staticmethod
    def _prepare_url(url: str) -> str:
        Hook._check_url(url)
        return url.strip("/")

    @abc.abstractmethod
    def _handle_data_write(self, url: str, data: _LazyCopy):
        """
        Handles the writing of the data. This method should be implemented by subclasses.

        Args:
            url (str): The url to write the data to.
            data (_LazyDeepCopy): The data to write. Note: This is a _LazyDeepCopy, so it must be unwrapped before use (see _LazyDeepCopy.data)
        """
        pass

    def _is_enabled_for(self, level: WriteLevel) -> bool:
        return self.level.value <= level.value

    def _handle_data_write_internal(self, url: str, data: Any):
        suffix = self._prepare_url(url)
        full_url = suffix if self.prefix == "" else f"{self.prefix}/{suffix}"
        self._handle_data_write(full_url, _LazyCopy(data))

    def extend_prefix(self, prefix: str):
        prefix = self._prepare_url(prefix)
        self._prefixes.append(prefix)

    def reduce_prefix(self):
        self._prefixes.pop()

    def reset(self):
        self._prefixes = []

    def on_finish(self):
        pass

    def debug(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.DEBUG):
            self._handle_data_write_internal(url, data)

    def info(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.INFO):
            self._handle_data_write_internal(url, data)

    def basic(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.BASIC):
            self._handle_data_write_internal(url, data)


_HOOKS = []


def add_hook(_hook: Hook, /):
    if not isinstance(_hook, Hook):
        raise TypeError(f"callback must be of type {Hook}, not {type(_hook)}")
    _HOOKS.append(_hook)


register_hook = add_hook  # alias


def remove_hook(_hook: Hook, /):
    _HOOKS.remove(_hook)


unregister_hook = remove_hook  # alias


def list_hooks() -> List[Hook]:
    return _HOOKS.copy()


def _apply_to_all(func_name, *args, **kwargs):
    for callback in _HOOKS:
        method = getattr(callback, func_name)
        method(*args, **kwargs)


def debug(url: str, data: Any):
    """
    Write data with level DEBUG to all callbacks. This usually writes everything.
    """
    _apply_to_all("debug", url, data)


def info(url: str, data: Any):
    """
    Write data with level INFO to all callbacks. This usually writes everything except debugging information.
    """
    _apply_to_all("info", url, data)


def basic(url: str, data: Any):
    """
    Write data with level BASIC to all callbacks. This usually writes only the most important information.
    """
    _apply_to_all("basic", url, data)


def reset():
    """
    Reset all callbacks.
    """
    _apply_to_all("reset")


def on_finish():
    """
    Signal all callbacks that the current run is finished. Could be used to write additional information or clean up.
    """
    _apply_to_all("on_finish")


def extend_prefix(prefix: str):
    """
    Extend the prefix of all callbacks. This is useful for grouping callback-urls together. See prefix_extender for a context manager that does this automatically.
    """
    _apply_to_all("extend_prefix", prefix)


def reduce_prefix():
    """
    Reduce the prefix of all callbacks. This is useful for grouping callback-urls together. See prefix_extender for a context manager that does this automatically.
    """
    _apply_to_all("reduce_prefix")


class prefix_extender(ContextDecorator):
    """
    Context manager that extends the prefix of the hook.

    Args:
        prefix: The prefix to extend the hooks prefix with.

    Example:
        >>> import explainer.util.hooks as hooks
        >>> with hooks.prefix_extender("ext1"):
        ...     hooks.info("test", "test_data") # info (url="ext1/test")

        >>> @hooks.prefix_extender("example/subexample")
        ... def test_func():
        ...     hooks.debug("test", "test_data") # debugging (url="example/subexample/test")
        ...     with hooks.prefix_extender("subsubexample"):
        ...         hooks.debug("test2", "test_data") # debugging (url="example/subexample/subsubexample/test2")
        ...
        >>> test_func()

    """

    def __init__(self, prefix: str):
        self._prefix = prefix

    def __enter__(self):
        extend_prefix(self._prefix)

    def __exit__(self, exc_type, exc_value, traceback):
        reduce_prefix()
