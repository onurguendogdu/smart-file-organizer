import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from config import APP_NAME, APP_VERSION
from organizer import organize_folder
from settings import load_settings, save_settings


class SmartFileOrganizerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.settings = load_settings()

        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry(
            self.settings.get(
                "window_geometry",
                "820x680",
            )
        )
        self.root.minsize(720, 600)
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application,
        )

        self.selected_folder = tk.StringVar(
            value=self.settings.get("last_folder", "")
        )
        self.include_subfolders = tk.BooleanVar(
            value=self.settings.get(
                "include_subfolders",
                False,
            )
        )
        self.status_text = tk.StringVar(
            value="Wähle einen Ordner aus."
        )
        self.progress_text = tk.StringVar(
            value="0 von 0 Dateien"
        )

        self.create_style()
        self.create_widgets()
        self.update_initial_status()

    def create_style(self) -> None:
        style = ttk.Style()

        if "vista" in style.theme_names():
            style.theme_use("vista")

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
        )

    def create_widgets(self) -> None:
        main_frame = ttk.Frame(
            self.root,
            padding=28,
        )
        main_frame.pack(
            fill="both",
            expand=True,
        )

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(
            fill="x",
            pady=(0, 24),
        )

        ttk.Label(
            header_frame,
            text=APP_NAME,
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text=(
                "Dateien automatisch und sicher "
                "nach Dateityp organisieren."
            ),
            style="Subtitle.TLabel",
        ).pack(
            anchor="w",
            pady=(4, 0),
        )

        folder_section = ttk.LabelFrame(
            main_frame,
            text="Ordner",
            padding=16,
        )
        folder_section.pack(
            fill="x",
            pady=(0, 16),
        )

        folder_row = ttk.Frame(folder_section)
        folder_row.pack(fill="x")

        self.folder_entry = ttk.Entry(
            folder_row,
            textvariable=self.selected_folder,
            font=("Segoe UI", 10),
        )
        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
        )

        ttk.Button(
            folder_row,
            text="Auswählen",
            command=self.select_folder,
        ).pack(side="right")

        options_row = ttk.Frame(folder_section)
        options_row.pack(
            fill="x",
            pady=(14, 0),
        )

        ttk.Checkbutton(
            options_row,
            text="Dateien aus Unterordnern einbeziehen",
            variable=self.include_subfolders,
        ).pack(anchor="w")

        self.organize_button = ttk.Button(
            main_frame,
            text="Dateien organisieren",
            style="Primary.TButton",
            command=self.start_organizing,
        )
        self.organize_button.pack(
            fill="x",
            pady=(0, 16),
            ipady=9,
        )

        progress_section = ttk.LabelFrame(
            main_frame,
            text="Fortschritt",
            padding=16,
        )
        progress_section.pack(
            fill="x",
            pady=(0, 16),
        )

        self.progress_bar = ttk.Progressbar(
            progress_section,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self.progress_bar.pack(fill="x")

        progress_info = ttk.Frame(progress_section)
        progress_info.pack(
            fill="x",
            pady=(8, 0),
        )

        ttk.Label(
            progress_info,
            textvariable=self.status_text,
        ).pack(
            side="left",
            anchor="w",
        )

        ttk.Label(
            progress_info,
            textvariable=self.progress_text,
        ).pack(
            side="right",
            anchor="e",
        )

        result_section = ttk.LabelFrame(
            main_frame,
            text="Ergebnis",
            padding=12,
        )
        result_section.pack(
            fill="both",
            expand=True,
        )

        result_frame = ttk.Frame(result_section)
        result_frame.pack(
            fill="both",
            expand=True,
        )

        self.result_text = tk.Text(
            result_frame,
            wrap="word",
            font=("Consolas", 10),
            state="disabled",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.result_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_text.yview,
        )
        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.result_text.configure(
            yscrollcommand=scrollbar.set
        )

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(
            fill="x",
            pady=(12, 0),
        )

        self.open_log_button = ttk.Button(
            footer_frame,
            text="Letzte Log-Datei öffnen",
            command=self.open_last_log,
            state="disabled",
        )
        self.open_log_button.pack(side="left")

        ttk.Label(
            footer_frame,
            text=f"Version {APP_VERSION}",
        ).pack(side="right")

        self.last_log_path: str | None = None

    def update_initial_status(self) -> None:
        folder = self.selected_folder.get().strip()

        if folder and Path(folder).is_dir():
            self.status_text.set(
                "Der zuletzt verwendete Ordner wurde geladen."
            )

    def select_folder(self) -> None:
        current_folder = self.selected_folder.get().strip()

        if not Path(current_folder).is_dir():
            current_folder = str(Path.home())

        folder = filedialog.askdirectory(
            title="Ordner auswählen",
            initialdir=current_folder,
        )

        if folder:
            self.selected_folder.set(folder)
            self.status_text.set(
                "Ordner ausgewählt."
            )

    def start_organizing(self) -> None:
        folder = self.selected_folder.get().strip()

        if not folder:
            messagebox.showwarning(
                "Kein Ordner ausgewählt",
                "Bitte wähle zuerst einen Ordner aus.",
            )
            return

        folder_path = Path(folder)

        if not folder_path.is_dir():
            messagebox.showerror(
                "Ungültiger Ordner",
                "Der ausgewählte Ordner existiert nicht.",
            )
            return

        recursive_text = (
            "\n\nDateien aus Unterordnern werden ebenfalls "
            "einbezogen."
            if self.include_subfolders.get()
            else ""
        )

        confirmed = messagebox.askyesno(
            "Sortierung bestätigen",
            "Die Dateien werden in passende "
            "Kategorieordner verschoben."
            f"{recursive_text}\n\n"
            "Möchtest du fortfahren?",
        )

        if not confirmed:
            return

        self.organize_button.configure(
            state="disabled"
        )
        self.open_log_button.configure(
            state="disabled"
        )

        self.progress_bar["value"] = 0
        self.progress_text.set("0 von 0 Dateien")
        self.status_text.set(
            "Dateien werden verarbeitet ..."
        )
        self.clear_results()
        self.root.update_idletasks()

        try:
            result = organize_folder(
                folder_path=folder,
                include_subfolders=(
                    self.include_subfolders.get()
                ),
                progress_callback=self.update_progress,
            )

            self.show_result(result)

        except (
            FileNotFoundError,
            NotADirectoryError,
            PermissionError,
        ) as error:
            messagebox.showerror(
                "Fehler",
                str(error),
            )
            self.status_text.set(
                "Der Vorgang konnte nicht abgeschlossen werden."
            )

        except Exception as error:
            messagebox.showerror(
                "Unerwarteter Fehler",
                "Es ist ein unerwarteter Fehler "
                f"aufgetreten:\n\n{error}",
            )
            self.status_text.set(
                "Ein unerwarteter Fehler ist aufgetreten."
            )

        finally:
            self.organize_button.configure(
                state="normal"
            )

    def update_progress(
        self,
        current: int,
        total: int,
        message: str,
    ) -> None:
        percentage = (
            100
            if total == 0
            else current / total * 100
        )

        self.progress_bar["value"] = percentage
        self.progress_text.set(
            f"{current} von {total} Dateien"
        )
        self.status_text.set(message)
        self.root.update_idletasks()

    def show_result(self, result: dict) -> None:
        total_found = result.get("total_found", 0)
        moved = result.get("moved", 0)
        statistics = result.get("statistics", {})
        errors = result.get("errors", [])
        duration = result.get("duration_seconds", 0)
        recursive = result.get("recursive", False)

        self.last_log_path = result.get("log")

        lines = [
            "SORTIERUNG ABGESCHLOSSEN",
            "=" * 52,
            "",
            f"Gefundene Dateien:    {total_found}",
            f"Verschobene Dateien:  {moved}",
            f"Fehler:                {len(errors)}",
            f"Dauer:                 {duration:.2f} Sekunden",
            f"Unterordner:           "
            f"{'Einbezogen' if recursive else 'Nicht einbezogen'}",
            "",
            "KATEGORIEN",
            "-" * 52,
        ]

        if statistics:
            longest_category = max(
                len(category)
                for category in statistics
            )

            for category, amount in statistics.items():
                lines.append(
                    f"{category.ljust(longest_category)} : "
                    f"{amount}"
                )
        else:
            lines.append(
                "Keine Dateien wurden verschoben."
            )

        if errors:
            lines.extend(
                [
                    "",
                    "FEHLER",
                    "-" * 52,
                    *errors,
                ]
            )

        if self.last_log_path:
            lines.extend(
                [
                    "",
                    "LOG-DATEI",
                    "-" * 52,
                    self.last_log_path,
                ]
            )

            self.open_log_button.configure(
                state="normal"
            )

        self.write_results(
            "\n".join(lines)
        )

        self.progress_bar["value"] = 100
        self.progress_text.set(
            f"{moved} von {total_found} Dateien verschoben"
        )
        self.status_text.set(
            "Sortierung erfolgreich abgeschlossen."
        )

        messagebox.showinfo(
            "Sortierung abgeschlossen",
            f"{moved} Dateien wurden organisiert.\n"
            f"{len(errors)} Fehler sind aufgetreten.",
        )

    def open_last_log(self) -> None:
        if not self.last_log_path:
            return

        log_path = Path(self.last_log_path)

        if not log_path.exists():
            messagebox.showerror(
                "Log-Datei nicht gefunden",
                "Die Log-Datei existiert nicht mehr.",
            )
            return

        try:
            os.startfile(log_path)

        except OSError as error:
            messagebox.showerror(
                "Log-Datei konnte nicht geöffnet werden",
                str(error),
            )

    def clear_results(self) -> None:
        self.result_text.configure(
            state="normal"
        )
        self.result_text.delete(
            "1.0",
            "end",
        )
        self.result_text.configure(
            state="disabled"
        )

    def write_results(self, text: str) -> None:
        self.result_text.configure(
            state="normal"
        )
        self.result_text.delete(
            "1.0",
            "end",
        )
        self.result_text.insert(
            "1.0",
            text,
        )
        self.result_text.configure(
            state="disabled"
        )

    def close_application(self) -> None:
        save_settings(
            {
                "last_folder": (
                    self.selected_folder.get().strip()
                ),
                "include_subfolders": (
                    self.include_subfolders.get()
                ),
                "window_geometry": (
                    self.root.geometry()
                ),
            }
        )

        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    SmartFileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()