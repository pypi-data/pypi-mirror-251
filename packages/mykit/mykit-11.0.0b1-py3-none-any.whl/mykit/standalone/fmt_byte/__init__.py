import math
import re
def _connum(num):
    res = re.match(r'^(?P<sign>\+|-)?[0]*(?P<int>\d+)(?:(?P<dec>\.\d*?)[0]*)?$', str(num))
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
def fmt_byte(bytes:int, /, precision:int=2, gap:int=1) -> str:
    """
    - `precision`: rounding precision
    - `gap`: gap (in spaces) between the number and the unit
    >>> in_byte(100)  
    >>> in_byte(1300)  
    >>> in_byte(1300, 0, 0)  
    >>> in_byte(1700, 0, 0)  
    - is from `mykit.kit.text`
    """
    GAP = ' '*gap
    if bytes == 0: return '0' + GAP + 'B'
    bytes = round(bytes)
    sign = ''
    if bytes < 0:
        bytes = abs(bytes)
        sign = '-'
    power = math.floor( math.log(bytes, 1024) )
    number = round( bytes / math.pow(1024, power), precision )
    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]
    return sign + _connum(number) + GAP + UNIT[power]