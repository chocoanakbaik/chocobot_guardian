"""Windows elevation helpers for Chocobot Guardian.

The module uses the normal Windows UAC mechanism. It never attempts to
bypass, suppress, or weaken Windows security controls.
"""

from __future__ import annotations

import ctypes
import os
import sys
from typing import Optional


ERROR_CANCELLED = 1223


def is_windows() -> bool:
    """Return True when running on Microsoft Windows."""
    return os.name == "nt"


def is_elevated() -> bool:
    """Return whether the current process has administrator privileges."""
    if not is_windows():
        return False

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def request_elevation(
    executable: Optional[str] = None,
    parameters: Optional[str] = None,
) -> bool:
    """Ask Windows to relaunch a process through the normal UAC prompt.

    Returns True when Windows accepted the elevation request. A False result
    means the request could not be started or the user did not approve it.
    No security feature is disabled or bypassed.
    """
    if not is_windows():
        return False

    executable = executable or sys.executable
    parameters = parameters if parameters is not None else " ".join(
        _quote_argument(argument) for argument in sys.argv[1:]
    )

    try:
        shell32 = ctypes.windll.shell32
        result = shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            parameters,
            None,
            1,
        )
        return int(result) > 32
    except (AttributeError, OSError, TypeError, ValueError):
        return False


def _quote_argument(argument: str) -> str:
    """Quote a command-line argument conservatively for Windows."""
    if not argument:
        return '""'
    if not any(character.isspace() or character in '"' for character in argument):
        return argument
    return '"' + argument.replace('"', '\\"') + '"'


__all__ = ["is_windows", "is_elevated", "request_elevation", "ERROR_CANCELLED"]
