import typing
import os
from pyldplayer._internal.callback import method_callback_decorator
from pyldplayer._utils.subprocess import subprocess_exec, subprocess_query

class LDConsoleProcMeta(type):
    _instances : typing.ClassVar[typing.Dict[str, "LDConsoleProc"]] = {}
    
    def __call__(cls, path : str):
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")
        
        if not (
            os.path.exists(path)
            and os.path.isfile(path)
            and os.path.basename(path) == "ldconsole.exe"
        ):
            raise RuntimeError("Could not find ldconsole.exe")
        
        path = os.path.abspath(path)
        
        if path not in cls._instances:
            cls._instances[path] = super(LDConsoleProcMeta, cls).__call__(path)
        return cls._instances[path]
    
class LDConsoleProc(metaclass=LDConsoleProcMeta):
    def __init__(self, path : str):
        self.__path = path
        query_res = self.query(no_filter=True)

        if query_res[0] != 'dnplayer Command Line Management Interface':
            raise RuntimeError("Invalid path")
        
    @property
    def path(self):
        return self.__path
        
    @property
    def folder(self):
        return os.path.dirname(self.path)
        
    @method_callback_decorator
    def query(self, command : str= None, *args, timeout : int = 10, no_filter : bool = False, leave_raw : bool = False):
        return subprocess_query(self.path, command, *args, timeout=timeout, no_filter=no_filter, leave_raw=leave_raw)
    
    @method_callback_decorator
    def exec(self, command : str, *args):
        return subprocess_exec(self.path, command, *args)
        
    def __hash__(self) -> int:
        return hash(self.path)