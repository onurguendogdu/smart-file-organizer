from pathlib import Path

from config import (
    DEFAULT_CATEGORY,
    FILE_TYPES,
    IGNORED_FILES,
    IGNORED_PREFIXES,
)


def should_ignore_file(file_path: Path) -> bool:
    """Return True when a file should not be processed."""
    file_name_lower = file_path.name.lower()

    if file_name_lower in IGNORED_FILES:
        return True

    return any(
        file_path.name.startswith(prefix)
        for prefix in IGNORED_PREFIXES
    )


def get_category(file_path: Path) -> str:
    """Determine the destination category using the file extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY


def get_unique_destination(destination: Path) -> Path:
    """
    Return a destination path that does not overwrite an existing file.

    Example:
    image.jpg
    image (1).jpg
    image (2).jpg
    """
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"

        if not candidate.exists():
            return candidate

        counter += 1