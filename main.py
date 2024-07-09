
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread
from pathlib import Path
import shutil

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorting")
        self.root.geometry("400x400")
        self.root.config(bg="light yellow")

        # Трансляції для кожної мови / Übersetzungen für jede Sprache / Translations for each language
        self.translations = {
            'EN': {
                'source_label': "Enter the source folder",
                'dest_label': "Enter the destination folder",
                'sort_button': "Sort",
                'status_success': "Files sorted",
                'status_error': "An error occurred",
                'lang_label': "Language"
            },
            'UK': {
                'source_label': "Введіть папку для сортування",
                'dest_label': "Введіть папку для результату",
                'sort_button': "Відсортувати",
                'status_success': "Файли відсортовано",
                'status_error': "Виникла помилка",
                'lang_label': "Мова"
            },
            'DE': {
                'source_label': "Geben Sie den Quellordner ein",
                'dest_label': "Geben Sie den Zielordner ein",
                'sort_button': "Sortieren",
                'status_success': "Dateien sortiert",
                'status_error': "Ein Fehler ist aufgetreten",
                'lang_label': "Sprache"
            }
        }

        self.language = tk.StringVar(value='EN')
        self.create_widgets()
        self.update_texts()

    def create_widgets(self):
        # Етикетка "Мова" / Beschriftung "Sprache" / Label "Language"
        language_frame = tk.Frame(self.root)
        language_frame.pack(anchor='ne', padx=10, pady=5)

        self.language_label = tk.Label(language_frame, text="Language:")  # "Мова:"
        self.language_label.pack(side='left')

        self.language_combobox = ttk.Combobox(language_frame, textvariable=self.language)
        self.language_combobox['values'] = ("EN", "UK", "DE")
        self.language_combobox.pack(side='left', padx=5)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)

        self.label_source = tk.Label(self.root, bg="light yellow", anchor='w')
        self.label_source.pack(fill='x', padx=10, pady=5)

        self.entry_source = tk.Entry(self.root, width=50)
        self.entry_source.pack(fill='x', padx=10, pady=5)

        self.label_dest = tk.Label(self.root, bg="light yellow", anchor='w')
        self.label_dest.pack(fill='x', padx=10, pady=5)

        self.entry_dest = tk.Entry(self.root, width=50)
        self.entry_dest.pack(fill='x', padx=10, pady=5)

        self.button_sort = tk.Button(self.root, command=self.start_sorting)
        self.button_sort.pack(pady=20)

        self.status_label = tk.Label(self.root, text="", bg="light yellow", anchor='w')
        self.status_label.pack(fill='x', padx=10, pady=20)

    def update_texts(self):
        # Оновлення текстів / Aktualisierung der Texte / Updating texts
        lang = self.language.get()
        self.label_source.config(text=self.translations[lang]['source_label'])
        self.label_dest.config(text=self.translations[lang]['dest_label'])
        self.button_sort.config(text=self.translations[lang]['sort_button'])
        self.language_label.config(text=self.translations[lang]['lang_label'])

    def change_language(self, event):
        # Зміна мови / Sprachwechsel / Changing language
        self.update_texts()

    def verzeichnisse(self, schlax_p, schlax_k, status_label):
        try:
            # Словник для відстеження вже створених підпапок
            created_dirs = {}

            # Створення об'єкту Path для цільової директорії
            directory = Path(schlax_k)
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)

            # Створення об'єкту Path для початкової директорії
            directory_1 = Path(schlax_p)

            if not directory_1.exists():
                raise FileNotFoundError(f"Директорія {schlax_p} не існує")

            # Виведення переліку всіх файлів та піддиректорій
            for path in directory_1.iterdir():
                if path.is_file():
                    suffix = path.suffix[1:]  # Видаляємо точку перед суфіксом

                    if suffix not in created_dirs:
                        # Створюємо підпапку для суфіксу, якщо вона ще не створена
                        directory_2 = directory / suffix
                        if not directory_2.exists():
                            directory_2.mkdir(parents=True, exist_ok=True)
                        created_dirs[suffix] = directory_2

                    # Вихідний і цільовий файли для копіювання
                    source = path
                    destination = created_dirs[suffix] / path.name

                    # Копіювання файлу
                    shutil.copy(source, destination)

                # Запускаємо рекурсію для глибокого пошуку
                if path.is_dir():
                    self.verzeichnisse(path, directory, status_label)

            status_label.config(text=self.translations[self.language.get()]['status_success'], bg="green")

        except FileNotFoundError as e:
            status_label.config(text=self.translations[self.language.get()]['status_error'], bg="red")
            messagebox.showerror("Error", f"Error: {e}")
        except PermissionError as e:
            status_label.config(text=self.translations[self.language.get()]['status_error'], bg="red")
            messagebox.showerror("Error", f"Error: Permission denied: {e}")
        except Exception as e:
            status_label.config(text=self.translations[self.language.get()]['status_error'], bg="red")
            messagebox.showerror("Error", f"Error: {e}")

    def start_sorting(self):
        schlax_p = self.entry_source.get()
        schlax_k = self.entry_dest.get()
        self.status_label.config(text="", bg="light yellow")
        thread = Thread(target=self.verzeichnisse, args=(schlax_p, schlax_k, self.status_label))
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()


