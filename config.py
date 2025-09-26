"""
Global configuration and environment variable loading.

This module centralizes configuration values such as service URLs,
login success/failure probes, and other runtime settings. Environment
variables are used when available, with sensible defaults.
"""

import os
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent
"""Path: Base directory of the project (the directory containing this config)."""

MSU_LOGIN_URL: str = os.getenv("MSU_LOGIN_URL", "https://lk.msu.ru/cabinet")
"""str: Login page URL for the MSU Cabinet system.

Defaults to ``https://lk.msu.ru/cabinet`` if the environment variable
``MSU_LOGIN_URL`` is not set.
"""

# -------------------
LOGIN_SUCCESS_PROBES: list[tuple[str, str]] = [
    ("link", "Оценки"),  # Presence of "Оценки" link indicates success
]
"""list[tuple[str, str]]: Probes to check for login success.

Each probe is a (by, selector) tuple to locate UI elements that only
appear on successful login.
"""

LOGIN_ERROR_PROBES: list[tuple[str, str]] = [
    ("css", ".alert-danger"),  # Bootstrap alert box
    ("css", ".invalid-feedback"),  # Invalid form field message
    ("css", ".help-block"),  # Generic form error block
]
"""list[tuple[str, str]]: Probes to check for login failure.

Each probe is a (by, selector) tuple to locate error messages
in the login page.
"""

LOGIN_POSTWAIT_SEC: int = 5
"""int: Maximum number of seconds to wait after clicking login before checking probes."""
