"""
Exception classes for wrapper-specific errors
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from numpy.typing import NDArray


class WrapperError(ValueError):
    """
    Base exception for errors that arise from wrapper
    """


class WrapperErrorUnknownCause(WrapperError):
    """
    Raised when there is an error with the wrapper, but we have nothing to help debug
    """

    def __init__(self, msg: str):
        suffix = "Underlying reason unknown"
        error_msg = f"{msg}. {suffix}."

        super().__init__(error_msg)


class InitialisationError(WrapperError):
    """
    Raised when the wrapper around the Fortran module hasn't been initialised yet
    """

    def __init__(self, model: Any, method: Optional[Callable[..., Any]] = None):
        if method:
            error_msg = f"{model} must be initialised before {method} is called"
        else:
            error_msg = f"model ({model:r}) is not initialized yet"

        super().__init__(error_msg)


class CompiledExtensionNotFoundError(ImportError):
    """
    Raised when a compiled extension can't be import i.e. found
    """

    def __init__(self, compiled_extension_name: str):
        error_msg = f"Could not find compiled extension {compiled_extension_name!r}"

        super().__init__(error_msg)


class BadPointerError(ValueError):
    """
    Raised when a pointer has a value we know is wrong
    """

    def __init__(self, pointer_value: Any, extra_info: str):
        error_msg = (
            f"The array pointer value is wrong ({pointer_value=}). "
            f"{extra_info}. "
            "Further underlying reason for the error is unknown."
        )

        super().__init__(error_msg)


class PointerArrayConversionError(ValueError):
    """
    Raised when we know a pointer has been incorrectly converted to an array
    """

    def __init__(
        self,
        array: NDArray[Any],
        ptr: int,
        expected_array_interface_data: tuple[int, bool],
    ):
        error_msg = (
            "The array pointer has been incorrectly converted to an numpy array. "
            f"We received {array.__array_interface__['data']=}. "
            f"The expected value is {expected_array_interface_data}. "
            f"Full context: {ptr=} {array.__array_interface__=}"
        )

        super().__init__(error_msg)


class RelativePythonModuleNotFoundError(ImportError):
    """
    Raised when a Python import configured by fgen fails
    """

    def __init__(
        self,
        requesting_python_module: str,
        requested: str,
        requested_from_python_module: str,
    ):
        """
        Initialise

        Parameters
        ----------
        requesting_python_module
            The Python module in which the ``import`` statement appears

        requested
            The thing that is being requested e.g. ``HelpfulType``

        requested_from_python_module
            The Python module from which ``requested`` is being imported e.g.
            ``source_module`` in
            ``from source_module import HelpfulType``
        """
        error_msg = (
            "There is something wrong with your fgen configuration for "
            f"{requesting_python_module!r}. "
            "Somewhere (likely in the `.yaml` file which is used to generate "
            f"{requesting_python_module!r} with fgen) you are specifying that "
            f"{requested!r} can be imported from "
            f"{requested_from_python_module!r}, but this is failing."
        )

        super().__init__(error_msg)
