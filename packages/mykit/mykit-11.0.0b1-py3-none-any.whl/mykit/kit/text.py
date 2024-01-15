import math as _math
import re as _re
from typing import (
    NoReturn as _NoReturn,
    Union as _Union
)
def connum(num: _Union[str, int, float], /) -> _Union[str, _NoReturn]:
    """
    connum (Concise Number).
    Displaying the number as is, without plus signs or extra zeroes, for the UI.
    ---
    - `ValueError` if `num` is not a number-like
    - `connum(3.0)` -> `'3'`
    - `connum('+03.500')` -> `'3.5'`
    """
    res = _re.match(r'^(?P<sign>\+|-)?[0]*(?P<int>\d+)(?:(?P<dec>\.\d*?)[0]*)?$', str(num))
    if res is None:
        raise ValueError(f'Invalid numeric input: {repr(num)}.')
    sign, int, dec = res.groups()
    if sign in (None, '+'):
        out = ''
    else:
        if (int == '0') and (dec in (None, '.')):
            out = ''
        else:
            out = '-'
    out += int
    if dec not in (None, '.'):
        out += dec
    return out
def byteFmt(__bytes: int, /) -> str:
    """in more readable byte format"""
    if __bytes == 0:
        return '0 B'
    exp = _math.floor(_math.log(abs(__bytes), 1024))
    val = round( __bytes / _math.pow(1024, exp), 2)
    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]
    return f'{val} {UNIT[exp]}'
def in_byte(bytes: int, /, precision: int = 2, gap: int = 1) -> str:
    """
    - `precision`: rounding precision
    - `gap`: gap (in spaces) between the number and the unit
    >>> in_byte(100)  
    >>> in_byte(1300)  
    >>> in_byte(1300, 0, 0)  
    >>> in_byte(1700, 0, 0)  
    - `in_byte` is the extended version of `mykit.kit.text.byteFmt`
    """
    GAP = ' '*gap
    if bytes == 0: return '0' + GAP + 'B'
    bytes = round(bytes)
    sign = ''
    if bytes < 0:
        bytes = abs(bytes)
        sign = '-'
    power = _math.floor( _math.log(bytes, 1024) )
    number = round( bytes / _math.pow(1024, power), precision )
    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]
    return sign + connum(number) + GAP + UNIT[power]
def num_approx(num:float, /, precision:int=1, gap:int=0) -> str:
    """
    Round a number down to K (thousand), M (million), B (billion), etc.
    ---
    - `precision`: rounding precision
    - `gap`: gap (in spaces) between the number and the unit
    >>> num_approx(999)  
    >>> num_approx(1000)  
    >>> num_approx(1001)  
    >>> num_approx(1_250_000)  
    >>> num_approx(1_250_000, 0, 1)  
    >>> num_approx(1_750_000, 0, 1)  
    """
    suffixes = [
        (1e3, ''),
        (1e6, 'K'),
        (1e9, 'M'),
        (1e12, 'B'),
        (1e15, 'T'),
        (1e18, 'q'),  
        (1e21, 'Q'),  
        (1e24, 's'),  
        (1e27, 'S'),  
    ]
    sign = ''
    if num < 0:
        num = abs(num)
        sign = '-'
    for divisor, suffix in suffixes:
        if num < divisor:
            n_format = f'{num*1000/divisor:.{precision}f}'
            break
    if precision > 0:
        n_format = n_format.rstrip('0').rstrip('.')
    GAP = ''
    if suffix != '':
        GAP = ' '*gap
    return sign + n_format + GAP + suffix
def num_round(number:int, /, keep:int=2, add_commas:bool=True) -> str:
    """
    Rounding number (see demo below).
    ---
    - `number`: The input number; floats are also accepted.
    - `keep`: number of the non-zero part (see demo below)
    - `add_commas`: separated the thousands with commas
    >>> num_round(12345, 1)  
    >>> num_round(12345, 2)  
    >>> num_round(12345, 3)  
    >>> num_round(12385, 3)  
    - `keep` value is clamped to a minimum of 1.
    """
    number = round(number)
    sign = ''
    if number < 0:
        number = abs(number)
        sign = '-'
    keep = min(len(str(number)), max(1, keep))
    power = len(str(number)) - keep
    scale = int( _math.pow(10, power) )
    rounded = round(number/scale)*scale
    if add_commas:
        rounded = f'{rounded:,}'
    else:
        rounded = str(rounded)
    return sign + rounded