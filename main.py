import pathlib
from tkinter import Tk, filedialog

from randomfiles.file_manager import FileManager
from randomfiles.ui import Main


def main():
    tk = Tk()
    selected_dir = filedialog.askdirectory(parent=tk)
    if selected_dir:
        fm = FileManager(pathlib.Path(selected_dir))
        Main(tk, fm)
        tk.mainloop()


if __name__ == '__main__':
    main()

