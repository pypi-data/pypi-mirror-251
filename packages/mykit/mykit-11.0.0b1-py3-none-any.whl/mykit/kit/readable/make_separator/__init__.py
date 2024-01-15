import os as _os
from typing import (
    Optional as _Optional
)
def make_separator(char:str='─', length:_Optional[int]=None, length_backup:int=21) -> str:
    r"""
    Equivalent to `char*_os.get_terminal_size()[0]`
    - `char`: the separator character (should be a single char)
    - `length`: the separator length
    - `length_backup`: Used with `length=None` when an `OSError` arises (check this function code for details)
    >>> sep = make_separator('─')
    >>> print(sep + 'hi\n' + sep)
    """
    if length is None:
        try:
            L = _os.get_terminal_size().columns
        except OSError:  
            L = length_backup
    else:
        L = length
    return char*L