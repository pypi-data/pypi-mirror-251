import sys as _sys
from typing import (
    Callable as _Callable
)
from mykit.kit.color import (
    Colored as _Colored,
    Hex as _Hex,
)
from mykit.kit.readable.box import box as _box
def _show_help_msg(software, version, repository, cmds):  
    H = 'show this message then exit'
    longest = max([len(i) for i in cmds.keys()])  
    cmds_help = ''
    for name, (_, desc) in cmds.items():
        cmds_help += f"   {_Colored(software + ' ' + name, _Hex.CORN)}{' '*(longest-len(name))} -> {_Colored(desc, _Hex.CORN)} \n"
    cmds_help += f"   {_Colored(software, _Hex.CORN)} {' '*longest} -> {_Colored(H, _Hex.CORN)} \n"
    msg = _box(
        '\n'
        ' Commands: \n'  
        f'{cmds_help}'
        '\n'
        f' Info:\n'
        f'   software  : {software} \n'  
        f'   version   : {version} \n'
        f'   repository: {repository} \n'
    )
    print('\n' + msg)
class SingleSimple:
    """
    A simple tool for parsing arguments from the command line, designed to accept just 1 positional argument.
    >>> myprogram 
    >>> myprogram command_1 
    >>> myprogram command_2 
    """
    def __init__(self, name:str, version:str, repo:str) -> None:
        """
        - `name`: software/program name
        - `version`: software version
        - `repo`: software source code
        - There is no validation process, such as checking if the command
            name should not be empty, should not be duplicated, etc. So
            please handle that manually.
        - Also, there are no extreme case validations, such as when no
            command was given, etc. Please handle it manually.
        """
        self.name = name
        self.version = version
        self.repo = repo
        self.cmds = {}
    def add(self, cmd:str, run:_Callable[[], None], desc:str) -> None:
        """
        - `cmd`: command name (which will be used like `myprogram <cmd>`)
        - `run`: function to be fired when `cmd` executed
        - `desc`: description of the command
        """
        self.cmds[cmd] = [run, desc]
    def _run_inner(self, args, is_testing):  
        if len(args) == 1:
            _show_help_msg(self.name, self.version, self.repo, self.cmds)
            if is_testing: return
            _sys.exit(0)
        cmd = args[1]
        if cmd not in self.cmds:
            print(f'Unknown commands {repr(cmd)}, run `{self.name}` for help.')
            if is_testing: return
            _sys.exit(1)
        self.cmds[cmd][0]()
    def run(self) -> None:
        """Listen to the command line and run the requested command."""
        args = _sys.argv
        self._run_inner(args, False)