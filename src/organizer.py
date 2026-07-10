import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Callable

from config import (
    CATEGORY_NAMES,
    LOG_DIRECTORY_NAME,
)
from file_utils import (
    get_category,
    get_unique_destination,
    should_ignore_file,
)

ProgressCallback = Callable[[int, int, str], None]


def collect_files(
    root_folder: Path,
    include_subfolders: bool,
) -> list[Path]:
    """Collect processable files from the selected folder."""
    files: list[Path] = []

    if include_subfolders:
        candidates = root_folder.rglob("*")
    else:
        candidates = root_folder.iterdir()

    for candidate in candidates:
        if not candidate.is_file():
            continue

        if should_ignore_file(candidate):
            continue

        relative_parts = candidate.relative_to(root_folder).parts

        if relative_parts:
            top_level_name = relative_parts[0]

            if top_level_name in CATEGORY_NAMES:
                continue

            if top_level_name == LOG_DIRECTORY_NAME:
                continue

        files.append(candidate)

    return sorted(
        files,
        key=lambda path: str(path).lower(),
    )


def create_log_file(
    root_folder: Path,
    started_at: datetime,
    finished_at: datetime,
    moved_entries: list[str],
    statistics: Counter,
    errors: list[str],
) -> Path:
    """Create a detailed log file for the completed operation."""
    log_directory = root_folder / LOG_DIRECTORY_NAME
    log_directory.mkdir(exist_ok=True)

    timestamp = started_at.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_directory / f"organization_{timestamp}.log"

    duration = finished_at - started_at

    lines = [
        "SMART FILE ORGANIZER",
        "",
        f"Started:  {started_at:%Y-%m-%d %H:%M:%S}",
        f"Finished: {finished_at:%Y-%m-%d %H:%M:%S}",
        f"Duration: {duration.total_seconds():.2f} seconds",
        "",
        "MOVED FILES",
        "-" * 70,
    ]

    if moved_entries:
        lines.extend(moved_entries)
    else:
        lines.append("No files were moved.")

    lines.extend(
        [
            "",
            "STATISTICS",
            "-" * 70,
        ]
    )

    if statistics:
        for category, amount in sorted(statistics.items()):
            lines.append(f"{category}: {amount}")
    else:
        lines.append("No category statistics available.")

    lines.extend(
        [
            "",
            f"Total moved: {sum(statistics.values())}",
            f"Errors: {len(errors)}",
        ]
    )

    if errors:
        lines.extend(
            [
                "",
                "ERRORS",
                "-" * 70,
                *errors,
            ]
        )

    log_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return log_file


def organize_folder(
    folder_path: str,
    include_subfolders: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """Organize files in the selected folder."""
    root_folder = Path(folder_path).expanduser().resolve()

    if not root_folder.exists():
        raise FileNotFoundError(
            "Der ausgewählte Ordner wurde nicht gefunden."
        )

    if not root_folder.is_dir():
        raise NotADirectoryError(
            "Der ausgewählte Pfad ist kein Ordner."
        )

    started_at = datetime.now()
    files = collect_files(
        root_folder,
        include_subfolders,
    )

    total_files = len(files)
    statistics: Counter = Counter()
    moved_entries: list[str] = []
    errors: list[str] = []

    for index, file_path in enumerate(files, start=1):
        category = get_category(file_path)
        target_directory = root_folder / category
        target_directory.mkdir(exist_ok=True)

        destination = get_unique_destination(
            target_directory / file_path.name
        )

        try:
            original_relative_path = file_path.relative_to(root_folder)

            shutil.move(
                str(file_path),
                str(destination),
            )

            statistics[category] += 1

            moved_entries.append(
                f"{original_relative_path} -> "
                f"{destination.relative_to(root_folder)}"
            )

            message = f"{file_path.name} -> {category}"

        except (OSError, shutil.Error) as error:
            error_message = f"{file_path}: {error}"
            errors.append(error_message)
            message = f"Fehler bei {file_path.name}"

        if progress_callback is not None:
            progress_callback(
                index,
                total_files,
                message,
            )

    finished_at = datetime.now()

    log_file = create_log_file(
        root_folder=root_folder,
        started_at=started_at,
        finished_at=finished_at,
        moved_entries=moved_entries,
        statistics=statistics,
        errors=errors,
    )

    return {
        "total_found": total_files,
        "moved": sum(statistics.values()),
        "statistics": dict(sorted(statistics.items())),
        "errors": errors,
        "log": str(log_file),
        "duration_seconds": (
            finished_at - started_at
        ).total_seconds(),
        "recursive": include_subfolders,
    }