from time import sleep
import typing
from pyldplayer._utils.subprocess import subprocess_exec, subprocess_query
from pyldplayer.console import LDConsole
from pyldplayer.consoleInstance import LDConsoleInstance
import os
import io
from PIL import Image

class AdbConsole:
    def __init__(self, console : LDConsole | str):
        if not isinstance(console, str):
            self.__console = console
            self.__path = os.path.join(console._LDConsole__console.folder, "adb.exe")
        else:
            self.__console = None
            self.__path = console
            
        self.adbDevices()
        
    @property
    def path(self):
        return self.__path    
    
    def adbDevices(self, maxCount = 2):
        count = 0
        while True:
            count = count + 1
            if count > 1:
                sleep(0.2)
            
            maxCount = maxCount - 1

            if maxCount < 0:
                break
            
            x1= subprocess_query(self.path, "devices", timeout=3)
            
            if len(x1) == 0:
                continue
                
            if x1[0] != "List of devices attached":
                continue
            
            return [x.split("\t")[0] for x in x1[1:]]
    
    def __getitem__(self, id):
        return AdbInstance(self.__console[id], self)

        
class AdbInstance:
    def __init__(self, ins : LDConsoleInstance, _console : AdbConsole):
        self.__instance = ins
        self.__console = _console
        
        self.__adb_mode : typing.Literal["console", "adb"] = "console"
        self.__device_bind = None
        
    def __consoleProc__(self):
        return self.__console._AdbConsole__proc
    
    @property
    def mode(self):
        return self.__adb_mode
    
    @mode.setter
    def mode(self, value : typing.Literal["console", "adb"]):
        self.__adb_mode = value
        
    @property
    def deviceName(self):
        return self.__device_bind
    
    @deviceName.setter
    def deviceName(self, value : str):
        self.__device_bind = value
        
    def _exec(self, command : str):
        if self.__adb_mode == "console":
            self.__instance.adb(command)
        else:
            cmdlines = command.split()
            subprocess_exec(self.__console.path, cmdlines[0], "-s", self.deviceName,*cmdlines[1:])
        
    def _query(self, command : str, raw : bool = False):
        if self.__adb_mode == "console":
            return self.__instance.adb(command, raw)
        else:
            return subprocess_query(self.__console.path, "-s", self.deviceName, command, leave_raw=raw)
    
    def openApp(self, package : str):
        self._exec(f"shell monkey -p {package} -c android.intent.category.LAUNCHER 1")
    
    def swipe(self, x1, y1, x2, y2):
        self._exec(f"shell input swipe {x1} {y1} {x2} {y2}")
        

    

    