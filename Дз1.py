import tkinter as tk
from tkinter import messagebox
from threading import Thread
from pathlib import Path
import shutil

def verzeichnisse(schlax_p, schlax_k, status_label):
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
                verzeichnisse(path, directory, status_label)

        status_label.config(text="Файли відсортовано", bg="green")

    except FileNotFoundError as e:
        status_label.config(text="Виникла помилка", bg="red")
        messagebox.showerror("Помилка", f"Помилка: {e}")
    except PermissionError as e:
        status_label.config(text="Виникла помилка", bg="red")
        messagebox.showerror("Помилка", f"Помилка: Немає дозволу на доступ: {e}")
    except Exception as e:
        status_label.config(text="Виникла помилка", bg="red")
        messagebox.showerror("Помилка", f"Інша помилка: {e}")

def start_sorting():
    schlax_p = entry_source.get()
    schlax_k = entry_dest.get()
    status_label.config(text="", bg="light yellow")
    thread = Thread(target=verzeichnisse, args=(schlax_p, schlax_k, status_label))
    thread.start()

root = tk.Tk()
root.title("Сортування файлів")
root.geometry("400x400")
root.config(bg="light yellow")

# Поле для введення шляху до файлів
label_source = tk.Label(root, text="Введіть файл для сортування", bg="light yellow")
label_source.pack(pady=5)

entry_source = tk.Entry(root, width=50)
entry_source.pack(pady=5)

# Поле для введення шляху до цільової директорії
label_dest = tk.Label(root, text="Введіть папку у яку буде завантажено результат", bg="light yellow")
label_dest.pack(pady=5)

entry_dest = tk.Entry(root, width=50)
entry_dest.pack(pady=5)

# Кнопка для запуску сортування
button_sort = tk.Button(root, text="Відсортувати", command=start_sorting)
button_sort.pack(pady=20)

# Статус
status_label = tk.Label(root, text="", bg="light yellow")
status_label.pack(pady=20)

root.mainloop()



