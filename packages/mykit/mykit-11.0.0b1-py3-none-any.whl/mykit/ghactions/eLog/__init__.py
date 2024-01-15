import enum as _enum
import subprocess as _sp
from mykit.kit.color import (
    Colored as _Colored,
    Hex as _Hex,
)
from mykit.kit.time import TimeFmt as _TimeFmt
class _Level(_enum.IntEnum):
    QUIET = 0
    _ADDONS = 50  
    ERROR = 100
    WARNING = 200
    INFO = 300
    DEBUG = 400
class eL:
    """
    eL (`echo` Log): A simple logger using `echo` function,
    intended for use within GitHub Action virtual machines.
    Inspired by `mykit.kit.pLog.pL`.
    """
    _testing = False  
    level = _Level.DEBUG  
    @classmethod
    def set_level(cls, level:str, /) -> None:
        """
        `level`:
        - `'quiet'`
        - `'error'`
        - `'warning'`
        - `'info'`
        - `'debug'`
        """
        try:
            cls.level = getattr(_Level, str(level).upper())
        except AttributeError:
            raise ValueError(f'Invalid level value: {repr(level)}.')
    @classmethod
    def _echo(cls, text, level:_Level):
        if level <= cls.level:
            if cls._testing: print(text)
            else: _sp.run(['echo', text])
    @classmethod
    def group(cls, name:str, /) -> None:
        cls._echo(f'::group::{name}', _Level._ADDONS)
    @classmethod
    def endgroup(cls, name:str='', /) -> None:
        """
        - `name`: doesn't do anything, just for readability.
        >>> eL.group('group-a')
        >>> eL.endgroup()
        >>> eL.group('group-b')
        >>> eL.endgroup('group-b')
        """
        cls._echo('::endgroup::', _Level._ADDONS)
    @classmethod
    def _logger(cls, level:_Level, color, msg):
        text = f'[{_TimeFmt.hour()}] {_Colored(level.name, color)}: {msg}'
        cls._echo(text, level)
    @classmethod
    def debug(cls, msg:str, /) -> None:
        cls._logger(_Level.DEBUG, _Hex.WHEAT, msg)
    @classmethod
    def info(cls, msg:str, /) -> None:
        cls._logger(_Level.INFO, _Hex.BLUE_GRAY, msg)
    @classmethod
    def warning(cls, msg:str, /) -> None:
        cls._logger(_Level.WARNING, _Hex.DARK_ORANGE, msg)
    @classmethod
    def error(cls, msg:str, /) -> None:
        cls._logger(_Level.ERROR, _Hex.SCARLET, msg)