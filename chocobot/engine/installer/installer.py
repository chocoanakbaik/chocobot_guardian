"""Transparent application installation engine for Chocobot Guardian.

The installer is deliberately conservative: it validates paths, creates only
its own destination directory, copies application files, and verifies the
result. It does not disable Defender, SmartScreen, UAC, firewall controls, or
any other Windows security mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os
import shutil
from typing import Iterable, Optional

from .elevation import is_elevated, is_windows, request_elevation


@dataclass(frozen=True)
class InstallationResult:
    """Structured result returned by an installation attempt."""

    success: bool
    message: str
    destination: Optional[Path] = None
    installed_files: tuple[Path, ...] = field(default_factory=tuple)
    requires_elevation: bool = False


def install_application(
    source_directory: str | os.PathLike[str],
    destination_directory: str | os.PathLike[str],
    *,
    require_elevation: bool = True,
) -> InstallationResult:
    """Install application files from a source directory.

    This function performs an explicit filesystem installation. If elevation
    is required and the process is not elevated, it requests Windows UAC and
    returns without copying files. The caller can then coordinate the elevated
    process and continue the installation.

    Source and destination must not resolve to the same directory.
    """
    source = _resolve_directory(source_directory)
    destination = _resolve_destination(destination_directory)

    validation_error = _validate_paths(source, destination)
    if validation_error:
        return InstallationResult(False, validation_error, destination=destination)

    if require_elevation and is_windows() and not is_elevated():
        return InstallationResult(
            False,
            "Installation requires Windows administrator permission.",
            destination=destination,
            requires_elevation=True,
        )

    try:
        destination.mkdir(parents=True, exist_ok=True)
        installed_files = _copy_tree(source, destination)
        _verify_installation(source, destination, installed_files)
    except (OSError, ValueError) as exc:
        return InstallationResult(
            False,
            f"Installation failed: {exc}",
            destination=destination,
        )

    return InstallationResult(
        True,
        "Installation completed and verified successfully.",
        destination=destination,
        installed_files=tuple(installed_files),
    )


def request_installation_elevation() -> bool:
    """Request UAC elevation for the current application process."""
    if not is_windows() or is_elevated():
        return is_elevated()
    return request_elevation()


def _resolve_directory(value: str | os.PathLike[str]) -> Path:
    return Path(value).expanduser().resolve()


def _resolve_destination(value: str | os.PathLike[str]) -> Path:
    return Path(value).expanduser().resolve()


def _validate_paths(source: Path, destination: Path) -> Optional[str]:
    if not source.exists():
        return "Installation source directory does not exist."
    if not source.is_dir():
        return "Installation source is not a directory."
    if source == destination:
        return "Installation source and destination cannot be the same directory."

    try:
        destination.relative_to(source)
    except ValueError:
        pass
    else:
        return "Installation destination cannot be inside the source directory."

    if not any(source.iterdir()):
        return "Installation source directory is empty."

    return None


def _copy_tree(source: Path, destination: Path) -> list[Path]:
    """Copy files while preserving the relative directory structure."""
    installed: list[Path] = []

    for item in source.rglob("*"):
        relative = item.relative_to(source)
        target = destination / relative

        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        if not item.is_file():
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        installed.append(target)

    return installed


def _verify_installation(
    source: Path,
    destination: Path,
    installed_files: Iterable[Path],
) -> None:
    """Verify that every copied file exists and has the expected size."""
    checked = 0
    for target in installed_files:
        relative = target.relative_to(destination)
        original = source / relative

        if not target.exists() or not target.is_file():
            raise OSError(f"Installed file is missing: {relative}")
        if target.stat().st_size != original.stat().st_size:
            raise OSError(f"Installed file size mismatch: {relative}")
        checked += 1

    if checked == 0:
        raise OSError("No application files were installed.")


__all__ = [
    "InstallationResult",
    "install_application",
    "request_installation_elevation",
]
