"""Windows compatibility for gltest's fd-backed stdin injector.

The installed gltest release unlinks an open temporary file. Windows keeps
that handle locked; leaving the short-lived file for the OS cleanup does not
alter contract execution.
"""
import os

_unlink = os.unlink
def _windows_safe_unlink(path, *args, **kwargs):
    try:
        return _unlink(path, *args, **kwargs)
    except PermissionError:
        if 'AppData\\Local\\Temp' in str(path):
            return None
        raise
os.unlink = _windows_safe_unlink
