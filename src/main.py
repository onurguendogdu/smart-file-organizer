import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from organizer import organize_folder


class SmartFileOrganizerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("760x620")
        self.root.minsize(680, 540)

        self.selected_folder = tk.StringVar()
        self.status_text = tk.StringVar(
            value="Wähle einen Ordner aus, den du organisieren möchtest."
        )

        self.create_widgets()

    def create_widgets(self) -> None:
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="Smart File Organizer",
            font=("Segoe UI", 22, "bold"),
        )
        title.pack(pady=(0, 6))

        subtitle = ttk.Label(
            main_frame,
            text="Sortiert Dateien automatisch nach ihrem Dateityp.",
            font=("Segoe UI", 11),
        )
        subtitle.pack(pady=(0, 24))

        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill="x")

        folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.selected_folder,
            font=("Segoe UI", 10),
        )
        folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        select_button = ttk.Button(
            folder_frame,
            text="Ordner auswählen",
            command=self.select_folder,
        )
        select_button.pack(side="right")

        self.organize_button = ttk.Button(
            main_frame,
            text="DATEIEN ORGANISIEREN",
            command=self.start_organizing,
        )
        self.organize_button.pack(fill="x", pady=20, ipady=8)

        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self.progress_bar.pack(fill="x")

        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=("Segoe UI", 10),
        )
        status_label.pack(anchor="w", pady=(8, 14))

        result_label = ttk.Label(
            main_frame,
            text="Ergebnis",
            font=("Segoe UI", 12, "bold"),
        )
        result_label.pack(anchor="w")

        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.result_text = tk.Text(
            result_frame,
            height=16,
            wrap="word",
            font=("Consolas", 10),
            state="disabled",
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
        scrollbar.pack(side="right", fill="y")

        self.result_text.configure(yscrollcommand=scrollbar.set)

    def select_folder(self) -> None:
        folder = filedialog.askdirectory(
            title="Ordner auswählen",
            initialdir=str(Path.home()),
        )

        if folder:
            self.selected_folder.set(folder)
            self.status_text.set(f"Ausgewählt: {folder}")

    def start_organizing(self) -> None:
        folder = self.selected_folder.get().strip()

        if not folder:
            messagebox.showwarning(
                "Kein Ordner ausgewählt",
                "Bitte wähle zuerst einen Ordner aus.",
            )
            return

        confirmation = messagebox.askyesno(
            "Dateien organisieren",
            "Die Dateien werden in passende Unterordner verschoben.\n\n"
            "Möchtest du fortfahren?",
        )

        if not confirmation:
            return

        self.organize_button.configure(state="disabled")
        self.progress_bar["value"] = 0
        self.clear_results()
        self.status_text.set("Dateien werden verarbeitet ...")
        self.root.update_idletasks()

        try:
            result = organize_folder(
                folder,
                progress_callback=self.update_progress,
            )

            self.show_result(result)

        except FileNotFoundError as error:
            messagebox.showerror("Fehler", str(error))
            self.status_text.set("Der Ordner wurde nicht gefunden.")

        except NotADirectoryError as error:
            messagebox.showerror("Fehler", str(error))
            self.status_text.set("Der ausgewählte Pfad ist kein Ordner.")

        except PermissionError:
            messagebox.showerror(
                "Keine Berechtigung",
                "Auf mindestens eine Datei oder einen Ordner konnte "
                "nicht zugegriffen werden.",
            )
            self.status_text.set("Keine ausreichende Berechtigung.")

        except Exception as error:
            messagebox.showerror(
                "Unerwarteter Fehler",
                f"Es ist ein unerwarteter Fehler aufgetreten:\n{error}",
            )
            self.status_text.set("Ein unerwarteter Fehler ist aufgetreten.")

        finally:
            self.organize_button.configure(state="normal")

    def update_progress(
        self,
        current: int,
        total: int,
        message: str,
    ) -> None:
        percentage = 100 if total == 0 else current / total * 100

        self.progress_bar["value"] = percentage
        self.status_text.set(f"{current}/{total}: {message}")
        self.root.update_idletasks()

    def show_result(self, result: dict) -> None:
        total_found = result.get("total_found", 0)
        moved = result.get("moved", 0)
        statistics = result.get("statistics", {})
        errors = result.get("errors", [])
        log_path = result.get("log")

        lines = [
            "Sortierung abgeschlossen",
            "=" * 48,
            "",
            f"Gefundene Dateien:   {total_found}",
            f"Verschobene Dateien: {moved}",
            "",
            "Kategorien:",
        ]

        if statistics:
            longest_category = max(len(category) for category in statistics)

            for category, amount in sorted(statistics.items()):
                lines.append(
                    f"  {category.ljust(longest_category)} : {amount}"
                )
        else:
            lines.append("  Keine Dateien verschoben.")

        if errors:
            lines.extend(
                [
                    "",
                    f"Fehler: {len(errors)}",
                ]
            )

            for error in errors:
                lines.append(f"  {error}")

        if log_path:
            lines.extend(
                [
                    "",
                    "Log-Datei:",
                    f"  {log_path}",
                ]
            )

        self.write_results("\n".join(lines))

        self.progress_bar["value"] = 100
        self.status_text.set(
            f"Fertig: {moved} Dateien wurden organisiert."
        )

        messagebox.showinfo(
            "Sortierung abgeschlossen",
            f"{moved} Dateien wurden organisiert.\n\n"
            f"Log-Datei:\n{log_path or 'Keine Log-Datei erstellt.'}",
        )

    def clear_results(self) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.configure(state="disabled")

    def write_results(self, text: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")


def main() -> None:
    root = tk.Tk()

    style = ttk.Style()

    if "vista" in style.theme_names():
        style.theme_use("vista")

    SmartFileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()