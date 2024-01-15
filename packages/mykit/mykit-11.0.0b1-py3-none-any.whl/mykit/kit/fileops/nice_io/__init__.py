import os as _os
from typing import (
    Optional as _Optional,
    Tuple as _Tuple,
    List as _List,
    Union as _Union,
)
from mykit.kit.fileops.simple import (
    norm_pth as _norm_pth,
    dont_worry_the_path_ends_with as _dont_worry_the_path_ends_with,
    definitely_a_file as _definitely_a_file,
    definitely_a_dir as _definitely_a_dir,
    this_path_must_not_exist as _this_path_must_not_exist,
)
class NiceIO:
    """Procedurally strict for performing file operations like read, write, and rewrite"""
    @staticmethod
    def read(file_path:str, /, suffixes:_Optional[_Union[str, _List[str], _Tuple[str, ...]]]=None) -> str:
        """
        Get the content of the given file path
        - `suffixes`: Guarantee reading from the expected file (e.g., making sure reading a Python file by setting `suffixes='.py'`).
                      If `None`, the path's endings will not be checked.
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        _definitely_a_file(path_normalized)
        if suffixes is not None: _dont_worry_the_path_ends_with(path_normalized, suffixes)
        with open(path_normalized, 'r') as fp:
            out = fp.read()
        return out
    @staticmethod
    def write(file_path:str, content:str, suffixes:_Optional[_Union[str, _List[str], _Tuple[str, ...]]]=None) -> None:
        """
        Write the given `content` into a new file
        - `content`: the file contents
        - `suffixes`: Guarantee the expected file (e.g., making sure it's a Python file by setting `suffixes='.py'`)
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        if suffixes is not None: _dont_worry_the_path_ends_with(path_normalized, suffixes)
        _definitely_a_dir(_os.path.dirname(path_normalized))
        _this_path_must_not_exist(path_normalized)
        with open(path_normalized, 'w') as fp:
            fp.write(content)
    @staticmethod
    def rewrite(file_path:str, new_content:str, suffixes:_Optional[_Union[str, _List[str], _Tuple[str, ...]]]=None) -> None:
        """
        Replace the existing file at `file_path` with the `new_content`
        - `new_content`: the file contents
        - `suffixes`: Guarantee the expected file (e.g., making sure it's a Python file by setting `suffixes='.py'`)
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'
        if suffixes is not None: _dont_worry_the_path_ends_with(path_normalized, suffixes)
        _definitely_a_file(path_normalized)
        _this_path_must_not_exist(tmp_path)
        _this_path_must_not_exist(bak_path)
        with open(tmp_path, 'w') as fp: fp.write(new_content)  
        _os.rename(path_normalized, bak_path)                  
        _os.rename(tmp_path, path_normalized)                  
        _os.remove(bak_path)                                   
    @staticmethod
    def recover(file_path:str, /, suffixes:_Optional[_Union[str, _List[str], _Tuple[str, ...]]]=None) -> None:
        """
        Try to fix the broken file, mostly because of interrupted or sudden
        stops when performing the `.rewrite` method above. Note that this is still
        not fully optimized and might still change in the future.
        - `suffixes`: Guarantee the expected file (e.g., making sure it's a Python file by setting `suffixes='.py'`)
        - Please manually inspect this function for all possible exceptions
        """
        path_normalized = _norm_pth(file_path)
        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'
        if suffixes is not None: _dont_worry_the_path_ends_with(path_normalized, suffixes)
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
    @staticmethod
    def erase(file_path:str, /, suffixes:_Optional[_Union[str, _List[str], _Tuple[str, ...]]]=None) -> None:
        """
        ⚠️ Clear the file's content.
        - `suffixes`: Guarantee the expected file (e.g., making sure it's a Python file by setting `suffixes='.py'`)
        - Please manually inspect this function for all possible exceptions
        """
        NiceIO.rewrite(file_path, '', suffixes)