# file_manager_backend.py
import os
import subprocess
from tkinter import messagebox


class FileManagerBackend:
    def __init__(self):
        self.current_directory = ""
