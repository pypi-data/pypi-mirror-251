import functools
import inspect
import logging
import sys
import time
import traceback
from typing import TypeVar, ParamSpec, Type, Iterable, Callable

R = TypeVar("R")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


class MaxRetryError(Exception):
    pass


def inspect_full_name(cls_or_func: Callable) -> str:
    _module = inspect.getmodule(cls_or_func).__name__
    if _module == 'builtins':
        return cls_or_func.__name__
    else:
        return _module + '.' + cls_or_func.__name__


def retry(retry_types: Iterable[Type[Exception]], interval: Iterable[int] = (1, 3, 5,)):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _err = []

            for _int in interval:
                try:
                    return func(*args, **kwargs)
                except tuple(retry_types) as e:
                    stack = traceback.extract_tb(sys.exc_info()[2])[1:]
                    stack_list = traceback.format_list(stack)
                    _err.append(e)
                    time.sleep(_int)
                    logger.debug(f"function will retry after {_int}s for error{stack_list}")
                    continue
            raise MaxRetryError(f"Max retry limited reached for function {inspect_full_name(func)}")

        return wrapper

    return decorator
