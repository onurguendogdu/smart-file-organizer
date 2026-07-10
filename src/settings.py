import json
from pathlib import Path

from config import APP_DATA_DIRECTORY, SETTINGS_FILE


DEFAULT_SETTINGS = {
    "last_folder": "",
    "include_subfolders": False,
    "window_geometry": "820x680",
}


def load_settings() -> dict:
    """Load saved application settings."""
    settings = DEFAULT_SETTINGS.copy()

    if not SETTINGS_FILE.exists():
        return settings

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            saved_settings = json.load(file)

        if isinstance(saved_settings, dict):
            settings.update(saved_settings)

    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()

    return settings


def save_settings(settings: dict) -> None:
    """Save application settings in the user's home directory."""
    APP_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    temporary_file = Path(f"{SETTINGS_FILE}.tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(
                settings,
                file,
                indent=2,
                ensure_ascii=False,
            )

        temporary_file.replace(SETTINGS_FILE)

    except OSError:
        if temporary_file.exists():
            temporary_file.unlink(missing_ok=True)