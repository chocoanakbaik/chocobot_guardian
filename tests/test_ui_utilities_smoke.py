"""Smoke-test construction of the working utility pages on a desktop runner."""
import os
import tkinter as tk

import pytest

from chocobot.app import ChocobotApp


pytestmark = pytest.mark.skipif(
    os.name != "nt" and not os.environ.get("DISPLAY"),
    reason="A graphical desktop display is required for Tkinter UI smoke tests.",
)


def test_working_utility_pages_build_without_user_interaction():
    app = ChocobotApp()
    app.root.withdraw()
    pages = [
        app.page_security,
        app.page_link,
        app.page_files,
        app.page_system,
        app.page_network,
        app.page_monitor,
    ]
    try:
        for page_builder in pages:
            parent = tk.Frame(app.root)
            parent.pack(fill="both", expand=True)
            page_builder(parent)
            app.root.update_idletasks()
            parent.destroy()
            app.root.update_idletasks()
    finally:
        app.root.destroy()
