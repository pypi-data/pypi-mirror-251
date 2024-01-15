from datetime import datetime, timedelta, timezone
import sys
from typing import NoReturn
import os
def exit_on_error(message:str, gmt:float=None, Ctxt=None) -> NoReturn:  
    """
    Exit with error code 1.
    - `message`: Error message.
    - `gmt`: GMT offset (in hours). Example: if UTC+0100 -> gmt=1; UTC-0230 -> gmt=-2.5.
             If `None`, will use local machine timezone.
    - `Ctxt`: for printing in color. This is a function from mykit lib for text-coloring.
    """
    strf = 'EXITED ON ERROR @ %H:%M:%S'
    if gmt is None:
        T = datetime.now().astimezone().strftime(strf)
    else:
        T = datetime.now().astimezone(timezone(timedelta(hours=gmt))).strftime(strf)
    PAD = 2  
    SEP = '^'*((os.get_terminal_size().columns-1-len(T)-PAD)//2)
    footer = f'{SEP} {T} {SEP}'
    if Ctxt is None:
        FOOTER = footer
    else:
        FOOTER = Ctxt(footer, '
    print('─'*(os.get_terminal_size().columns-1) + '\n' + message + '\n' + FOOTER)
    sys.exit(1)