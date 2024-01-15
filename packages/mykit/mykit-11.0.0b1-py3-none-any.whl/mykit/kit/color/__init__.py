import os as _os
import re as _re
import sys as _sys
from typing import (
    Optional as _Optional,
    Tuple as _Tuple
)
def interpolate_color(color1: str, color2: str, x: float) -> str:
    """
    Interpolates between two colors based on the given ratio `x`.
    ---
    - `color1`: The first color in hexadecimal format (e.g., '
    - `color2`: The second color in hexadecimal format (e.g., '
    - `x`: The ratio determining the interpolation between the two colors. Should be between 0 and 1.
    - The interpolated color as a hexadecimal string.
    >>> interpolate_color('
    '
    >>> interpolate_color('
    '
    >>> interpolate_color('
    '
    """
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = round(r1 + (r2 - r1)*x)
    g = round(g1 + (g2 - g1)*x)
    b = round(b1 + (b2 - b1)*x)
    interpolated_color = f'
    return interpolated_color
def getgray(alpha: float, /, max_lum: int = 255) -> str:
    """
    Returns a hexadecimal color value representing a grayscale shade based on the given alpha and maximum luminance.
    ---
    - `alpha`: A grayscale shade intensity value in the range [0, 1].
    - `max_lum`: Maximum luminance value for grayscale in the range [0, 255].
    >>> getgray(0.5)
    '
    """
    a = f'{round(max_lum*alpha):02x}'
    return f'
def hex_to_rgb(hex_color: str, /) -> _Tuple[int, int, int]:
    hex_color = hex_color.lstrip('
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def rgb_to_hex(r: int, g: int, b: int, /) -> str:
    return f'
def hexa_to_hex(foreground: str, opacity: float, background: str) -> str:
    """
    Calculates the hexadecimal color code of `foreground` with the given `opacity` on `background`.
    The `foreground` and `background` must be valid hexadecimal color codes,
    and the `opacity` value must be in the interval [0, 1].
    """
    fg = [int(foreground[i:i+2], 16) for i in (1, 3, 5)]
    bg = [int(background[i:i+2], 16) for i in (1, 3, 5)]
    r = round(fg[0]*opacity + bg[0]*(1 - opacity))
    g = round(fg[1]*opacity + bg[1]*(1 - opacity))
    b = round(fg[2]*opacity + bg[2]*(1 - opacity))
    return f'
def interpolate_with_black(foreground: str, opacity: float) -> str:
    """
    This is the optimized version of `hexa_to_hex(foreground, opacity, '
    Please refer to the documentation of the `hexa_to_hex` function for more details.
    """
    c = [int(foreground[i:i+2], 16) for i in (1, 3, 5)]
    r = round( c[0]*opacity )
    g = round( c[1]*opacity )
    b = round( c[2]*opacity )
    return f'
class Hex:
    """List of colors in hexadecimal format."""
    BLACK = '
    WHITE = '
    RED = '
    LIME = '
    BLUE = '
    YELLOW = '
    CYAN = '
    MAGENTA = '
    SILVER = '
    GRAY = '
    MAROON = '
    OLIVE = '
    GREEN = '
    PURPLE = '
    TEAL = '
    NAVY = '
    ALABASTER = '
    AMBER = '
    ARYLIDE_YELLOW = '
    ASH_GRAY = '
    ATOMIC_TANGERINE = '
    AUBURN = '
    AUREOLIN = '
    AZURE = '
    BEIGE = '
    BITTERSWEET = '
    BLACK_OLIVE = '
    BLEU_DE_FRANCE = '
    BLIZZARD_BLUE = '
    BLUE_GRAY = '
    BLUSH = '
    BOTTLE_GREEN = '
    BRIGHT_MAROON = '
    BURGUNDY = '
    BURNT_ORANGE = '
    BURNT_SIENNA = '
    CADMIUM_ORANGE = '
    CAMEL = '
    CAPRI = '
    CARDINAL = '
    CARIBBEAN_GREEN = '
    CAROLINA_BLUE = '
    CHAMPAGNE = '
    CITRINE = '
    CORAL = '
    CORN = '
    DARK_ORANGE = '
    DARK_RED = '
    DIM_GRAY = '
    ELECTRIC_BLUE = '
    EMERALD = '
    FALU_RED = '
    FLAME = '
    FIREBRICK = '
    GO_GREEN = '
    GRANITE_GRAY = '
    HARLEQUIN = '
    IVORY = '
    JADE = '
    LAPIS_LAZULI = '
    LAVENDER_GRAY = '
    LAWN_GREEN = '
    LIGHT_GRAY = '
    LIGHT_GREEN = '
    LIGHT_YELLOW = '
    LILAC = '
    LINEN = '
    LISERAN_PURPLE = '
    MANATEE = '
    MAUVE = '
    MYSTIC = '
    OPAL = '
    OUTRAGEOUS_ORANGE = '
    PEACH = '
    RASPBERRY = '
    RUBY = '
    RUST = '
    SAND = '
    SAPPHIRE = '
    SCARLET = '
    SEA_GREEN_CRAYOLA = '
    SEASHELL = '
    SUNGLOW = '
    TAN = '
    WHEAT = '
    TERMINAL = '
    GRAY30 = '
    LAVENDER_BLISS = '
class Colored:
    """
    >>> from mykit.kit.color import Colored, Hex
    >>> for k, v in Hex.__dict__.items():
    >>>     if k.startswith('__'): continue
    >>>     print(Colored(k, v))
    - This class will be deprecated soon, use `mykit.kit.color.ctxt` instead
    """
    _win_init = False  
    _RESET = '\033[0m'
    def __new__(
        cls,
        text:str,
        /,
        fg:str=Hex.MANATEE,
        bg:_Optional[str]=None
    ) -> str:
        """
        Return the colored version of `text`.
        ---
        - `fg`: foreground color in hexadecimal format
        - `bg`: background color in hexadecimal format; if not specified,
                the default terminal background color will be used.
        """
        if _sys.platform.lower() == 'win32':
            if not Colored._win_init:
                _os.system('color')
                Colored._win_init = True
        text = str(text)
        fg_r, fg_g, fg_b = hex_to_rgb(fg)
        header = (
            '\033['
            f'38;2;{fg_r};{fg_g};{fg_b}'
        )
        if bg is not None:
            bg_r, bg_g, bg_b = hex_to_rgb(bg)
            header += f';48;2;{bg_r};{bg_g};{bg_b}'
        header += 'm'
        if cls._RESET in text:
            text = text.replace(cls._RESET, header)
        return header + text + cls._RESET
def colored_len(text:str, /) -> int:
    """
    Count the text length produced by `Colored` (also works for nested `Colored`).
    >>> colored_len(Colored('hi'))  
    >>> colored_len('12'+ Colored('34') + '56')  
    >>> colored_len(Colored('12' + Colored('34', Hex.RED)))  
    """
    original_len = len(text)
    c1 = _re.findall(r'\033\[38;2;\d{1,3};\d{1,3};\d{1,3}(?:;48;2;\d{1,3};\d{1,3};\d{1,3})?m', text)
    c2 = _re.findall(r'\033\[0m', text)
    color_len = sum([len(i) for i in c1+c2])
    return original_len - color_len