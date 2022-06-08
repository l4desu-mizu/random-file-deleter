import logging
import pathlib
import weakref
from pathlib import Path
import random
from typing import Union, Set, Callable

logger = logging.getLogger(__name__)


class FileManagerObserveMessage:
    def __init__(self, item: pathlib.Path):
        self.item = item


class ObserveError(FileManagerObserveMessage):
    def __init__(self, item: pathlib.Path, error: Exception):
        super().__init__(item)
        self.error = error


class ObserveSuccess(FileManagerObserveMessage):
    pass


class Deletable:

    def __init__(self, path: pathlib.Path, observer: Callable[[FileManagerObserveMessage], None]):
        self._deletion = path
        self._observer = weakref.WeakMethod(observer)

    def delete(self):
        try:
            self._deletion.unlink()
        except (FileNotFoundError, PermissionError) as e:
            self._observer()(ObserveError(self._deletion, e))
        else:
            self._observer()(ObserveSuccess(self._deletion))

    def __str__(self):
        return str(self._deletion)


class FileManager:

    def __init__(self, path: Union[Path | str]):
        self._path = Path(path)
        self._deleted_files: Set[Path] = set()
        self._undeletable_files: Set[Path] = set()

    @property
    def root(self):
        return self._path.absolute()

    @property
    def remaining_files(self):
        return self.all_files - self.undeletable

    @property
    def all_files(self):
        return set(p.relative_to(self._path) for p in self._path.glob("**/*") if p.is_file())

    @property
    def deleted(self):
        return self._deleted_files

    @property
    def undeletable(self):
        return self._undeletable_files

    def get_random(self):
        return Deletable(random.choice(list(self.remaining_files)), self._delete_callback)

    def _delete_callback(self, message: FileManagerObserveMessage):
        if isinstance(message, ObserveError):
            self._undeletable_files.add(message.item)
        elif isinstance(message, ObserveSuccess):
            self._deleted_files.add(message.item)
        else:
            logger.warning("Whatever this is %s", message)
