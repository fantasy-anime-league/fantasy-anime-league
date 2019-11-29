from typing import Any, Callable
import warnings
import functools

FuncT = Callable[..., Any]


def deprecated(
    reason: str = "This function has been deprecated.",
) -> Callable[[FuncT], FuncT]:
    """
    This decorator marks functions as deprecated and sends a warning.
    """

    def decorator(func: FuncT) -> FuncT:
        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"Call to deprecated function {func.__name__}: {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapped

    return decorator
