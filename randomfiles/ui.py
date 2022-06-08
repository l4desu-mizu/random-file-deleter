import tkinter
from tkinter import Tk
from typing import Callable

from randomfiles.file_manager import FileManager, Deletable


class GameOverDialog:
    def __init__(self, parent: Tk):
        frame = tkinter.Toplevel(parent)
        frame.resizable(False, False)
        label = tkinter.Label(frame, text="You loose!")
        button = tkinter.Button(frame, text="Okay...", command=parent.quit)
        label.grid(row=0, column=0)
        button.grid(row=1, column=0)
        frame.pack_slaves()


class Main:

    def __init__(self, parent: Tk, file_manager: FileManager):
        self._tk = parent
        self._file_manager = file_manager
        self._path_var = tkinter.StringVar(parent)
        self._list_var = tkinter.StringVar(parent)
        self._deleted_var = tkinter.StringVar(parent)
        self._undeleted_var = tkinter.StringVar(parent)
        self._update_labels()
        text_path = tkinter.Label(parent, textvariable=self._path_var)
        text_list = tkinter.Label(parent, textvariable=self._list_var)
        text_delted = tkinter.Label(parent, textvariable=self._deleted_var)
        text_undelted = tkinter.Label(parent, textvariable=self._undeleted_var)
        button = tkinter.Button(parent, text="roll", command=self._roll)
        text_path.grid(row=0, column=0)
        text_list.grid(row=1, column=0)
        text_delted.grid(row=2, column=0)
        text_undelted.grid(row=3, column=0)
        button.grid(row=4, column=0)
        parent.pack_slaves()

    def _update_labels(self):
        self._path_var.set(f"In {self._file_manager.root}")
        self._list_var.set(f"Found {len(self._file_manager.remaining_files)} files.")
        self._deleted_var.set(f"Deleted {len(self._file_manager.deleted)} files.")
        self._undeleted_var.set(f"Could not delete {len(self._file_manager.undeletable)} files.")

    def _restore(self):
        self._update_labels()
        self._tk.deiconify()

    def _roll(self):
        self._tk.withdraw()
        try:
            delete_target = self._file_manager.get_random()
        except IndexError:
            GameOverDialog(self._tk)
        else:
            DeleteDialog(self._tk, self._restore, delete_target)
        self._update_labels()


class DeleteDialog:

    def __init__(self, parent: Tk, notify: Callable, path: Deletable):
        self._notify = notify
        self._frame = tkinter.Toplevel(parent)
        self._frame.resizable(False, False)
        button_panel = tkinter.Frame(self._frame)
        yes = tkinter.Button(button_panel, text="yes", command=self._button(path.delete))
        no = tkinter.Button(button_panel, text="no", command=self._button())
        text = tkinter.Label(self._frame, text=f"Do you want to delete {path}?")
        yes.grid(row=0, column=0)
        no.grid(row=0, column=1)
        text.grid(row=0, column=0)
        button_panel.grid(row=1, column=0)
        self._frame.pack_slaves()

    def _button(self, side_effect=None):
        def wrapper():
            try:
                if side_effect:
                    side_effect()
            finally:
                self._frame.destroy()
                self._notify()
        return wrapper
