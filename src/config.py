from pathlib import Path

APP_NAME = "Smart File Organizer"
APP_VERSION = "1.2.0"

FILE_TYPES = {
    "Bilder": {
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
        ".tiff", ".tif", ".heic", ".svg", ".ico",
    },
    "Dokumente": {
        ".pdf", ".txt", ".doc", ".docx", ".odt", ".rtf",
        ".xls", ".xlsx", ".ods", ".csv",
        ".ppt", ".pptx", ".odp", ".epub", ".md",
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv",
        ".flv", ".webm", ".mpeg", ".mpg", ".m4v",
    },
    "Musik": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".m4a", ".wma", ".opus",
    },
    "Archive": {
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".bz2", ".xz", ".tgz",
    },
    "Programme": {
        ".exe", ".msi", ".msix", ".appx", ".apk",
        ".bat", ".cmd", ".com",
    },
    "Quellcode": {
        ".py", ".java", ".c", ".cpp", ".cc", ".cxx",
        ".h", ".hpp", ".cs", ".js", ".ts", ".html",
        ".css", ".php", ".sql", ".sh", ".ps1",
        ".kt", ".swift", ".go", ".rs", ".rb",
    },
    "Daten und Konfiguration": {
        ".json", ".xml", ".yaml", ".yml", ".ini",
        ".cfg", ".conf", ".toml", ".fgo", ".fdb",
    },
    "Java und Pakete": {
        ".jar", ".war", ".whl", ".deb", ".rpm",
    },
    "Datenträger": {
        ".iso", ".img", ".dmg", ".vhd", ".vhdx",
    },
}

DEFAULT_CATEGORY = "Sonstiges"

IGNORED_PREFIXES = (
    ".~lock.",
    "~$",
)

IGNORED_FILES = {
    "desktop.ini",
    "thumbs.db",
}

CATEGORY_NAMES = set(FILE_TYPES) | {DEFAULT_CATEGORY}

APP_DATA_DIRECTORY = Path.home() / ".smart_file_organizer"
SETTINGS_FILE = APP_DATA_DIRECTORY / "settings.json"
LOG_DIRECTORY_NAME = "Smart File Organizer Logs"