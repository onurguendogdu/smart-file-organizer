import os
import shutil

from config import FILE_TYPES


def organize_folder(folder):

    if not os.path.exists(folder):
        print("❌ Ordner wurde nicht gefunden.")
        return

    print(f"\n📂 Ordner gefunden: {folder}\n")

    files = os.listdir(folder)

    if not files:
        print("Der Ordner ist leer.")
        return

    for file in files:

        file_path = os.path.join(folder, file)

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        target_folder = "Sonstiges"

        for category, extensions in FILE_TYPES.items():
            if extension in extensions:
                target_folder = category
                break

        destination = os.path.join(folder, target_folder)

        os.makedirs(destination, exist_ok=True)

        shutil.move(file_path, os.path.join(destination, file))

        print(f"✅ {file} → {target_folder}")

    print("\n🎉 Alle Dateien wurden erfolgreich sortiert!")