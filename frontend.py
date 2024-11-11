# file_manager_frontend.py
import tkinter as tk
from tkinter import filedialog
from backend import FileManagerBackend


class FileManagerFrontend:
    def __init__(self, root):
        self.root = root
        self.backend = FileManagerBackend()

        # Настройка окна
        self.root.title("Файловый менеджер")
        self.root.geometry("600x400")
