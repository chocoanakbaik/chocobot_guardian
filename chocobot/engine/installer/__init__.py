"""Chocobot Guardian installation engine.

This package provides transparent, Windows-native installation support.
Installation must never bypass Windows security controls or user consent.
"""

from .installer import InstallationResult, install_application

__all__ = ["InstallationResult", "install_application"]
