# file_manager_frontend.py
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
from backend import FileManagerBackend

class FileManagerFrontend:
    def __init__(self, root):
        self.root = root
        self.backend = FileManagerBackend()

        # Создаем основной каркас
        self.root.title("Файловый менеджер")
        self.root.geometry("800x500")

        # Левая панель для кнопок
        self.left_frame = tk.Frame(self.root, width=200, bg='lightgray')
        self.left_frame.pack(side="left", fill="y")

        # Правая панель для отображения файлов
        self.right_frame = tk.Frame(self.root, width=600)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Метка для отображения текущего пути над всем интерфейсом
        self.path_label = tk.Label(self.right_frame, text=f"Текущий путь: {self.backend.current_directory}", anchor="w", bg="lightgray", width=100)
        self.path_label.pack(side="top", fill="x")


        # Список файлов
        self.file_listbox = tk.Listbox(self.right_frame)
        self.file_listbox.pack(fill="both", expand=True)

        # Подключение события двойного клика для открытия файлов и папок
        self.file_listbox.bind("<Double-1>", self.on_double_click)

        # Начальное отображение файлов
        self.display_files()

        # Кнопки на левой панели
        self.create_buttons()

    def create_buttons(self):
        """Создает кнопки на левой панели для выполнения операций."""
        buttons = [
            ("Создать файл", self.create_file),
            ("Создать папку", self.create_directory),
            ("Переименовать", self.rename_item),
            ("Удалить", self.delete_item),
            ("Копировать", self.copy_item),
            ("Обновить", self.display_files),
            ("Выбрать папку", self.choose_directory),
            ("Изменить права", self.change_permissions),
        ]
        for (text, command) in buttons:
            button = tk.Button(self.left_frame, text=text, command=command, width=20)
            button.pack(pady=5)

        # Кнопки назад и вперед
        self.nav_frame = tk.Frame(self.left_frame)  # Дополнительный фрейм для кнопок навигации
        self.nav_frame.pack(side="bottom", fill="x", pady=10)

        # Кнопка "Назад"
        back_button = tk.Button(self.nav_frame, text="Назад", command=self.go_back, width=20)
        back_button.pack(side="top", padx=5)

        # Кнопка "Вперед"
        forward_button = tk.Button(self.nav_frame, text="Вперед", command=self.go_forward, width=20)
        forward_button.pack(side="top", padx=5)

    def change_permissions(self):
        """Изменяет права доступа для выбранного файла/папки."""
        selected = self.file_listbox.curselection()
        if selected:
            name = self.file_listbox.get(selected)
            item_path = os.path.join(self.backend.current_directory, name)

            # Запрашиваем у пользователя права доступа
            perms = simpledialog.askstring("Изменить права", f"Введите новые права для '{name}' (например, 755):")
            if perms:
                try:
                    self.backend.change_permissions(item_path, perms)
                    self.display_files()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось изменить права: {e}")

    def display_files(self):
        """Отображает файлы в текущей директории."""
        self.file_listbox.delete(0, tk.END)
        items = self.backend.get_items()
        for item in items:
            self.file_listbox.insert(tk.END, item)

        # Обновляем метку с текущим путем
        self.path_label.config(text=f"Текущий путь: {self.backend.current_directory}")

    def choose_directory(self):
        """Позволяет выбрать директорию."""
        directory = filedialog.askdirectory()
        if directory:
            self.backend.set_directory(directory)
            self.display_files()

    def create_file(self):
        filename = simpledialog.askstring("Создать файл", "Введите имя файла:")
        if filename:
            self.backend.create_file(filename)
            self.display_files()

    def create_directory(self):
        dirname = simpledialog.askstring("Создать папку", "Введите имя папки:")
        if dirname:
            self.backend.create_directory(dirname)
            self.display_files()

    def rename_item(self):
        selected = self.file_listbox.curselection()
        if selected:
            old_name = self.file_listbox.get(selected)
            new_name = simpledialog.askstring("Переименовать", f"Новое имя для '{old_name}':")
            if new_name:
                self.backend.rename_item(old_name, new_name)
                self.display_files()

    def delete_item(self):
        selected = self.file_listbox.curselection()
        if selected:
            name = self.file_listbox.get(selected)
            confirm = messagebox.askyesno("Удалить", f"Вы уверены, что хотите удалить '{name}'?")
            if confirm:
                self.backend.delete_item(name)
                self.display_files()

    def copy_item(self):
        selected = self.file_listbox.curselection()
        if selected:
            name = self.file_listbox.get(selected)
            destination = filedialog.askdirectory(title="Выберите папку для копирования")
            if destination:
                self.backend.copy_item(name, destination)
                self.display_files()

    def go_back(self):
        """Переходит на предыдущую директорию."""
        items = self.backend.go_back()
        if items is not None:
            self.display_files()

    def go_forward(self):
        """Переходит в следующую директорию."""
        items = self.backend.go_forward()
        if items is not None:
            self.display_files()

    def on_double_click(self, event):
        """Обрабатывает двойной клик на элементе списка."""
        selected = self.file_listbox.curselection()
        if selected:
            item_name = self.file_listbox.get(selected)
            item_path = os.path.join(self.backend.current_directory, item_name)

            if os.path.isdir(item_path):  # Если это директория, переходим в нее
                self.backend.set_directory(item_path)
                self.display_files()
            else:  # Если это файл, открываем его
                self.open_file(item_path)

    def open_file(self, path):
        """Открывает файл с помощью системного приложения по умолчанию."""
        try:
            if os.name == 'posix':  # для MacOS и Linux
                subprocess.call(('xdg-open', path))
            elif os.name == 'nt':  # для Windows
                os.startfile(path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")