import json as _json
import os as _os
import subprocess as _sp
import sys as _sys
from typing import (
    Any as _Any
)
class SafeJSON:
    """Secure JSON read/write operations, ensuring data integrity during writing and rewriting."""
    @staticmethod
    def write(__pth: str, __obj: _Any, /, do_log: bool = True) -> None:
        pth_norm = _os.path.normpath(__pth)
        if not pth_norm.lower().endswith('.json'):
            raise AssertionError(f'Not a JSON file: {repr(__pth)}.')
        if not _os.path.isdir(_os.path.dirname(pth_norm)):
            raise NotADirectoryError(f'The directory does not exist: {repr(__pth)}.')
        if _os.path.exists(pth_norm):
            raise FileExistsError(f'File already exists: {repr(__pth)}.')
        with open(pth_norm, 'w') as fp:
            _json.dump(__obj, fp)
        if do_log:
            print(f'INFO: Json written: {repr(__pth)}.')
    @staticmethod
    def read(__pth: str, /) -> _Any:
        pth_norm = _os.path.normpath(__pth)
        if not pth_norm.lower().endswith('.json'):
            raise AssertionError(f'Not a JSON file: {repr(__pth)}.')
        if not _os.path.isfile(pth_norm):
            raise FileNotFoundError(f'Not a file: {repr(__pth)}.')
        with open(pth_norm, 'r') as fp:
            out = _json.load(fp)
        return out
    @staticmethod
    def rewrite(__pth: str, __obj: _Any, /, do_log: bool = True) -> None:
        pth_norm = _os.path.normpath(__pth)
        if not pth_norm.lower().endswith('.json'):
            raise AssertionError(f'Not a JSON file: {repr(__pth)}.')
        if not _os.path.isfile(pth_norm):
            raise FileNotFoundError(f'Not a file: {repr(__pth)}.')
        tmp_file = pth_norm + '.tmp'
        bak_file = pth_norm + '.bak'
        if _os.path.exists(tmp_file):
            raise FileExistsError(f'Temporary file exists: {repr(tmp_file)}.')
        if _os.path.exists(bak_file):
            raise FileExistsError(f'Backup file exists: {repr(bak_file)}.')
        with open(tmp_file, 'w') as fp:
            _json.dump(__obj, fp)
        _os.rename(pth_norm, bak_file)  
        _os.rename(tmp_file, pth_norm)  
        _os.remove(bak_file)  
        if do_log:
            print(f'INFO: Json rewritten: {repr(__pth)}.')
    @staticmethod
    def recover(__pth: str, /) -> None:
        pth_norm = _os.path.normpath(__pth)
        if not pth_norm.endswith('.json'):
            raise ValueError(f'Not a JSON file: {repr(__pth)}.')
        tmp_file = pth_norm + '.tmp'
        bak_file = pth_norm + '.bak'
        if _os.path.exists(pth_norm) and _os.path.exists(tmp_file) and (not _os.path.exists(bak_file)):
            _os.remove(tmp_file)
            return
        if (not _os.path.exists(pth_norm)) and _os.path.exists(tmp_file) and _os.path.exists(bak_file):
            _os.rename(tmp_file, pth_norm)
            _os.remove(bak_file)
            return
        if _os.path.exists(pth_norm) and (not _os.path.exists(tmp_file)) and _os.path.exists(bak_file):
            _os.remove(bak_file)
            return
def open_file(file_pth: str, /) -> None:
    """
    Opens a file using the default system application.
    ---
    - `NotImplementedError`: if the OS is unrecognizable
    """
    system = _sys.platform
    if system == 'win32':
        _os.startfile(file_pth)
    elif system == 'darwin':
        _sp.call(['open', file_pth])
    elif system.startswith('linux'):
        _sp.call(['xdg-open', file_pth])
    elif system.startswith('cygwin'):
        _sp.call(['cygstart', file_pth])
    else:
        raise NotImplementedError(f'Unsupported platform: {system}')