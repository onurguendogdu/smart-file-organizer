# Smart File Organizer

Smart File Organizer is a desktop application written in Python that automatically organizes files into categorized folders based on their file extensions.

The application provides an intuitive graphical user interface, automatic folder creation, duplicate file protection, progress tracking and detailed statistics after every run.

---

## Features

- Automatically organizes files into folders
- Supports over 70 different file extensions
- Graphical user interface built with Tkinter
- Automatic folder creation
- Duplicate file protection
- Progress bar during processing
- Summary statistics after every run
- Automatic categorization of:
  - Images
  - Documents
  - Videos
  - Music
  - Archives
  - Programs
  - Source Code
  - Configuration Files
  - Java Packages
  - Disk Images
  - Other Files
- Ignores temporary Office and Windows system files
- Clean and modular project structure

---

## Supported File Categories

| Category | Examples |
|----------|----------|
| Images | JPG, PNG, JPEG, GIF, WEBP, BMP, HEIC |
| Documents | PDF, DOCX, XLSX, PPTX, TXT, CSV |
| Videos | MP4, AVI, MKV, MOV |
| Music | MP3, WAV, FLAC, OGG |
| Archives | ZIP, RAR, 7Z |
| Programs | EXE, MSI, BAT |
| Source Code | PY, JAVA, CPP, C, JS, HTML, CSS, SQL |
| Configuration | JSON, XML, YAML, CFG |
| Java Packages | JAR, WAR |
| Disk Images | ISO, IMG, VHD |

---

## Screenshots

### Main Window

> Screenshot will be added soon.

### Result Window

> Screenshot will be added soon.

---

## Installation

Clone the repository

```bash
git clone https://github.com/onurguendogdu/smart-file-organizer.git
```

Navigate into the project

```bash
cd smart-file-organizer
```

Run the application

```bash
python src/main.py
```

---

## Project Structure

```text
smart-file-organizer/
│
├── docs/
├── screenshots/
├── src/
│   ├── config.py
│   ├── file_utils.py
│   ├── organizer.py
│   └── main.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Example

Before

```text
Downloads/

image.png
holiday.jpg
music.mp3
movie.mp4
document.pdf
program.exe
archive.zip
```

After

```text
Downloads/

Images/
    image.png
    holiday.jpg

Music/
    music.mp3

Videos/
    movie.mp4

Documents/
    document.pdf

Programs/
    program.exe

Archives/
    archive.zip
```

---

## Technologies

- Python 3
- Tkinter
- pathlib
- shutil
- Git
- GitHub

---

## Roadmap

### Version 1.1

- Dark Mode
- Better statistics
- Improved user interface
- Faster processing
- Better error handling

### Version 1.2

- Drag & Drop support
- Configuration file
- Logging
- Recursive folder organization

### Version 2.0

- Modern custom interface
- Multi-language support
- Automatic monitoring of folders
- Settings window
- Advanced filtering

---

## Future Improvements

- Custom categories
- File preview
- Undo operation
- Duplicate file detection
- Automatic scheduled organization
- Export statistics
- Search functionality

---

## License

This project is released under the MIT License.

---

## Author

Onur Gündogdu

Computer Science Student

Specialization: Artificial Intelligence