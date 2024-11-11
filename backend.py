#backend.py
import os
import shutil

class FileManagerBackend:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.history_back = []  # История путей назад
        self.history_forward = []  # История путей вперед
    def change_permissions(self, path, perms):
        """Изменяет права доступа для файла или директории."""
        try:
            perms = int(perms, 8)  # Конвертируем строку в число (например, 755)
            os.chmod(path, perms)  # Применяем права
        except ValueError:
            raise ValueError("Некорректные права доступа. Введите число в формате 755.")
    def set_directory(self, directory):
        """Устанавливает текущую директорию и очищает историю вперед."""
        if self.current_directory != directory:
            self.history_back.append(self.current_directory)
            self.history_forward.clear()  # Очистить историю вперед, если идет движение по пути вперед
        self.current_directory = directory
        return self.get_items()

    def go_back(self):
        """Возвращает в предыдущую директорию."""
        if self.history_back:
            self.history_forward.append(self.current_directory)
            self.current_directory = self.history_back.pop()
            return self.get_items()
        return None  # Если нет куда вернуться

    def go_forward(self):
        """Двигается вперед в следующую директорию, если такая есть."""
        if self.history_forward:
            self.history_back.append(self.current_directory)
            self.current_directory = self.history_forward.pop()
            return self.get_items()
        return None  # Если нет пути вперед

    def get_items(self):
        """Возвращает список файлов и каталогов в текущей директории."""
        return os.listdir(self.current_directory)

    def create_file(self, filename):
        """Создает новый файл в текущей директории."""
        open(os.path.join(self.current_directory, filename), 'w').close()

    def create_directory(self, dirname):
        """Создает новый каталог в текущей директории."""
        os.mkdir(os.path.join(self.current_directory, dirname))

    def rename_item(self, old_name, new_name):
        """Переименовывает файл или каталог."""
        os.rename(
            os.path.join(self.current_directory, old_name),
            os.path.join(self.current_directory, new_name)
        )

    def delete_item(self, name):
        """Удаляет файл или каталог."""
        path = os.path.join(self.current_directory, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def copy_item(self, name, destination):
        """Копирует файл или каталог в указанное место."""
        path = os.path.join(self.current_directory, name)
        dest_path = os.path.join(destination, name)
        if os.path.isdir(path):
            shutil.copytree(path, dest_path)
        else:
            shutil.copy2(path, dest_path)
