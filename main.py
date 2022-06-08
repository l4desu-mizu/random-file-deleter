import pathlib
from tkinter import Tk, filedialog

from randomfiles.file_manager import FileManager
from randomfiles.ui import Main


def main(path: str):
    fm = FileManager(pathlib.Path(path))
    tk = Tk()
    tk.resizable(False, False)
    Main(tk, fm)
    tk.mainloop()


if __name__ == '__main__':
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        main(selected_dir)

