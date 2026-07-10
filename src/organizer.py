from collections import Counter
from datetime import datetime
from pathlib import Path
import shutil

from file_utils import (
    get_category,
    get_unique_destination,
    should_ignore_file,
)


def organize_folder(folder_path, progress_callback=None):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError("Folder not found.")

    files = [
        file
        for file in folder.iterdir()
        if file.is_file() and not should_ignore_file(file)
    ]

    statistics = Counter()

    logs = []

    total = len(files)

    for index, file in enumerate(files, start=1):

        category = get_category(file)

        destination_folder = folder / category

        destination_folder.mkdir(exist_ok=True)

        destination = get_unique_destination(destination_folder / file.name)

        shutil.move(file, destination)

        statistics[category] += 1

        logs.append(
            f"{file.name} -> {category}"
        )

        if progress_callback:
            progress_callback(
                index,
                total,
                file.name
            )

    log_folder = folder / "logs"

    log_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = log_folder / f"{timestamp}.log"

    with open(log_file, "w", encoding="utf-8") as f:

        f.write("SMART FILE ORGANIZER\n\n")

        f.write(f"Date: {datetime.now()}\n\n")

        f.write("Moved Files\n")

        f.write("-------------------------\n")

        for line in logs:
            f.write(line + "\n")

        f.write("\n")

        f.write("Statistics\n")

        f.write("-------------------------\n")

        for category, amount in statistics.items():
            f.write(f"{category}: {amount}\n")

    return {
        "total_found": total,
        "moved": total,
        "statistics": dict(statistics),
        "errors": [],
        "log": str(log_file),
    }