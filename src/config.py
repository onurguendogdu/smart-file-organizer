FILE_TYPES = {
    "Bilder": {
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
        ".tiff", ".heic", ".svg", ".ico"
    },
    "Dokumente": {
        ".pdf", ".txt", ".doc", ".docx", ".odt", ".rtf",
        ".xls", ".xlsx", ".ods", ".csv",
        ".ppt", ".pptx", ".odp", ".epub"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv",
        ".flv", ".webm", ".mpeg", ".mpg"
    },
    "Musik": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".m4a", ".wma"
    },
    "Archive": {
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".bz2", ".xz"
    },
    "Programme": {
        ".exe", ".msi", ".msix", ".appx", ".apk",
        ".bat", ".cmd", ".com"
    },
    "Quellcode": {
        ".py", ".java", ".c", ".cpp", ".cc", ".cxx",
        ".h", ".hpp", ".cs", ".js", ".ts", ".html",
        ".css", ".php", ".sql", ".sh", ".ps1",
        ".kt", ".swift", ".go", ".rs"
    },
    "Daten und Konfiguration": {
        ".json", ".xml", ".yaml", ".yml", ".ini",
        ".cfg", ".conf", ".toml", ".fgo", ".fdb"
    },
    "Java und Pakete": {
        ".jar", ".war", ".whl", ".deb", ".rpm"
    },
    "Datenträger": {
        ".iso", ".img", ".dmg", ".vhd", ".vhdx"
    },
}

DEFAULT_CATEGORY = "Sonstiges"

# Diese temporären Dateien sollen nicht verschoben werden.
IGNORED_PREFIXES = (
    ".~lock.",
    "~$",
)

IGNORED_FILES = {
    "desktop.ini",
    "thumbs.db",
}