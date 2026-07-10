from pathlib import Path

from config import (
    DEFAULT_CATEGORY,
    FILE_TYPES,
    IGNORED_FILES,
    IGNORED_PREFIXES,
)


def should_ignore_file(file_path: Path) -> bool:
    file_name_lower = file_path.name.lower()

    if file_name_lower in IGNORED_FILES:
        return True

    return any(file_path.name.startswith(prefix) for prefix in IGNORED_PREFIXES)


def get_category(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY


def get_unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix

    counter = 1

    while True:
        new_destination = parent / f"{stem} ({counter}){suffix}"

        if not new_destination.exists():
            return new_destination

        counter += 1


def format_statistics(statistics: dict) -> str:
    if not statistics:
        return "No files were moved."

    longest = max(len(category) for category in statistics)

    lines = []

    for category, amount in statistics.items():
        lines.append(f"{category.ljust(longest)} : {amount}")

    return "\n".join(lines)