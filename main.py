# main.py
import tkinter as tk
from frontend import FileManagerFrontend

def main():
    root = tk.Tk()
    app = FileManagerFrontend(root)
    root.mainloop()

if __name__ == "__main__":
    main()