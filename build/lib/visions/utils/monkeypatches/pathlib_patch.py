# type: ignore
from pathlib import Path


def _copy(self, target):
    """Monkeypatch for pathlib

    Args:
        self:
        target:

    Returns:

    """
    import shutil

    assert self.is_file()
    shutil.copy(str(self), str(target))  # str() only there for Python < (3, 6)


Path.copy = _copy
