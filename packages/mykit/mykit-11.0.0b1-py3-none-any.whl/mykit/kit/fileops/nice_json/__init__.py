import json as _json
import os as _os
from typing import (
    Any as _Any,
)
from mykit.kit.fileops.simple import (
    norm_pth as _norm_pth,
    dont_worry_the_path_ends_with as _dont_worry_the_path_ends_with,
    definitely_a_file as _definitely_a_file,
    definitely_a_dir as _definitely_a_dir,
    this_path_must_not_exist as _this_path_must_not_exist
)
class NiceJSON:
    """Procedurally strict for performing file operations like read, write, and rewrite"""
    @staticmethod
    def read(file_path:str, /) -> _Any:
        """
        Get the content of the given JSON file path
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        _definitely_a_file(path_normalized)
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        with open(path_normalized, 'r') as fp:
            out = _json.load(fp)
        return out
    @staticmethod
    def write(file_path:str, content:_Any) -> None:
        """
        Write the given `content` into a new JSON file
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        _definitely_a_dir(_os.path.dirname(path_normalized))
        _this_path_must_not_exist(path_normalized)
        with open(path_normalized, 'w') as fp:
            _json.dump(content, fp)
    @staticmethod
    def rewrite(file_path:str, content:_Any) -> None:
        """
        Replace the existing JSON file at `file_path` with the new `content`
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        _definitely_a_file(path_normalized)
        _this_path_must_not_exist(tmp_path)
        _this_path_must_not_exist(bak_path)
        with open(tmp_path, 'w') as fp: _json.dump(content, fp)  
        _os.rename(path_normalized, bak_path)                    
        _os.rename(tmp_path, path_normalized)                    
        _os.remove(bak_path)                                     
    @staticmethod
    def recover(file_path:str, /) -> None:
        """
        Try to fix the broken JSON file, mostly because of interrupted or sudden
        stops when performing `NiceJSON.rewrite` above. Note that this is still
        not fully optimized and might still change in the future.
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        if _os.path.exists(path_normalized) and _os.path.exists(tmp_path) and (not _os.path.exists(bak_path)):
            _os.remove(tmp_path)
            return
        if (not _os.path.exists(path_normalized)) and _os.path.exists(tmp_path) and _os.path.exists(bak_path):
            _os.rename(tmp_path, path_normalized)
            _os.remove(bak_path)
            return
        if _os.path.exists(path_normalized) and (not _os.path.exists(tmp_path)) and _os.path.exists(bak_path):
            _os.remove(bak_path)
            return