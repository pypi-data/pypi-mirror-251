    
from types import MappingProxyType
from pyldplayer._internal._interfaces.ldconsoleI import LDConsoleI
from pyldplayer.consoleProc import LDConsoleProc
import typing
from pyldplayer.modifyConfig import LDModifyConfigDict
from pyldplayer.consoleInstance import LDConsoleInstance

class LDConsole(LDConsoleI):
    __console : LDConsoleProc
    __instances : typing.Dict[int, LDConsoleInstance]
    
    def __init__(self, ldw : LDConsoleProc):
        if isinstance(ldw, str):
            ldw = LDConsoleProc(ldw)
        self.__console = ldw
        self.__instances = {}
        
    def __hash__(self) -> int:
        return hash(self.__ldw)
    
    def __resolve_id(self, id : typing.Union[str, int]):
        args = []
        if isinstance(id, str):
            args.append("--name")
            args.append(id)
        else:
            args.append("--index")
            args.append(str(id))
        return args
    
    def quit(self, id : typing.Union[str, int]): 
        self.__console.exec("quit", *self.__resolve_id(id))

    def quitall(self):
        self.__console.exec("quitall")

    def launch(self, id : typing.Union[str, int]):
        self.__console.exec("launch", *self.__resolve_id(id))

    def reboot(self, id : typing.Union[str, int]):
        self.__console.exec("reboot", *self.__resolve_id(id))

    def list(self):
        return self.__console.query("list")

    def runninglist(self): 
        return self.__console.query("runninglist")

    def isrunning(self, id : typing.Union[str, int]):
        res = self.__console.query("isrunning", *self.__resolve_id(id))
        if res[0] == "stop":
            return False
        elif res[0] == "running":
            return True
        return res
    
    def list2(self)-> typing.Dict[int, LDConsoleInstance]:
        res = self.__console.query("list2")
        
        for line in res:
            if not line:
                continue

            spliited =line.split(",")
            x_id, x_name, \
                x_top_window_handle, x_bind_window_handle, \
                x_android_started_int, x_pid, x_pid_of_vbox = spliited[0:7]
            x_id = int(x_id)
            x_top_window_handle = int(x_top_window_handle)
            x_bind_window_handle = int(x_bind_window_handle)
            x_android_started_int = int(x_android_started_int)
            x_pid = int(x_pid)
            x_pid_of_vbox = int(x_pid_of_vbox)

            others = spliited[7:]

            if x_id not in self.__instances:
                self.__instances[x_id] = LDConsoleInstance(
                    id = x_id,
                    name = x_name,
                    top_window_handle = x_top_window_handle,
                    bind_window_handle = x_bind_window_handle,
                    android_started_int = x_android_started_int,
                    pid = x_pid,
                    pid_of_vbox = x_pid_of_vbox,
                    _console = self,
                    _others = others
                )
            else:
                ins = self.__instances[x_id]
                object.__setattr__(ins, 'name', x_name)
                object.__setattr__(ins, 'top_window_handle', x_top_window_handle)
                object.__setattr__(ins, 'bind_window_handle', x_bind_window_handle)
                object.__setattr__(ins, 'android_started_int', x_android_started_int)
                object.__setattr__(ins, 'pid', x_pid)
                object.__setattr__(ins, 'pid_of_vbox', x_pid_of_vbox)
                object.__setattr__(ins, '_others', others)

        # get all instances via list
        listitems = self.__console.query("list")
        self.__instances = {k : v for k, v in self.__instances.items() if v.name in listitems}

        return MappingProxyType(self.__instances)

    def add(self, name : str = None): 
        if name is None:
            return self.__console.exec("add")
        else:
            return self.__console.exec("add", "--name", name)

    def copy(self, id : typing.Union[str, int], name : str = None): 
        if name is None:
            return self.__console.exec("copy", *self.__resolve_id(id))
        else:
            return self.__console.exec("copy", *self.__resolve_id(id), "--name", name)

    def remove(self, id : typing.Union[str, int]):
        return self.__console.exec("remove", *self.__resolve_id(id))

    def rename(self, id : typing.Union[str, int], name : str):
        return self.__console.exec("rename", *self.__resolve_id(id), "--title", name)

    def modify(self, id : typing.Union[str, int], **kwargs : typing.Unpack[LDModifyConfigDict]): 
        args = []
        for name in kwargs.keys():
            val = kwargs[name]
            if val == "auto":
                args += [f"--{name}", "auto"]
            elif isinstance(val, typing.Tuple):
                args += [f"--{name}", ",".join(map(str, val))]
            elif not isinstance(val, bool):
                args += [f"--{name}", str(val)]
            elif val:
                args += [f"--{name}", "1"]
            else:
                args += [f"--{name}", "0"]
        return self.__console.exec("modify", *self.__resolve_id(id), *args)

    def installapp(self, id : typing.Union[str, int], filename : str = None, packagename : str = None):
        if filename is not None:
            return self.__console.exec("installapp", *self.__resolve_id(id), "--filename", filename)
        elif packagename is not None:
            return self.__console.exec("installapp", *self.__resolve_id(id), "--packagename", packagename)
        else:
            raise ValueError("filename or packagename is required")

    def uninstallapp(self, id : typing.Union[str, int], packagename : str): 
        return self.__console.exec("uninstallapp", *self.__resolve_id(id), "--packagename", packagename)

    def runapp(self, id : typing.Union[str, int], packagename : str):
        return self.__console.exec("runapp", *self.__resolve_id(id), "--packagename", packagename)

    def killapp(self, id : typing.Union[str, int], packagename : str):
        return self.__console.exec("killapp", *self.__resolve_id(id), "--packagename", packagename)        

    def locate(self, id : typing.Union[str, int], lng : str, lat : str):
        return self.__console.exec("locate", *self.__resolve_id(id), "--LLI", f"{lng},{lat}")

    def adb(self, id : typing.Union[str, int], command : str, raw : bool = False):
        return self.__console.query("adb", *self.__resolve_id(id), "--command", command, leave_raw=raw)

    def setprop(self, id : typing.Union[str, int], key : str, value : str):
        return self.__console.exec(
            "setprop", *self.__resolve_id(id), "--key", key, "--value", value
        )

    def getprop(self, id : typing.Union[str, int], key : str):
        return self.__console.query("getprop", *self.__resolve_id(id), "--key", key)

    def downcpu(self, id : typing.Union[str, int], rate : int):
        # if not 0 -100
        if rate < 0 or rate > 100:
            raise ValueError("rate must be between 0 and 100")

        return self.__console.exec("downcpu", *self.__resolve_id(id), "--rate", str(rate))

    def backup(self, id : typing.Union[str, int], filepath : str):
        return self.__console.exec("backup", *self.__resolve_id(id), "--file", filepath)

    def restore(self, id : typing.Union[str, int], filepath : str):
        return self.__console.exec("restore", *self.__resolve_id(id), "--file", filepath)

    def action(self, id : typing.Union[str, int], key : str, value : str):
        return self.__console.exec("action", *self.__resolve_id(id), "--key", key, "--value", value)

    def scan(self, id : typing.Union[str, int], filepath : str):
        return self.__console.exec("scan", *self.__resolve_id(id), "--file", filepath)

    def sortwnd(self):
        return self.__console.exec("sortwnd")

    def zoomin(self): 
        return self.__console.exec("zoomin")

    def zoomout(self): 
        return self.__console.exec("zoomout")

    def pull(self, id : typing.Union[str, int], remote : str, local : str):
        return self.__console.exec("pull", *self.__resolve_id(id), "--remote", remote, "--local", local)

    def push(self, id : typing.Union[str, int], local : str, remote : str): 
        return self.__console.exec("push", *self.__resolve_id(id),"--remote", remote,  "--local", local,)

    def backupapp(self, id : typing.Union[str, int], filepath : str): 
        return self.__console.exec("backupapp", *self.__resolve_id(id), "--file", filepath)

    def restoreapp(self, id : typing.Union[str, int], filepath : str): 
        return self.__console.exec("restoreapp", *self.__resolve_id(id), "--file", filepath)

    def globalsetting(
        self, 
        fps : int = None,
        audio : bool = None, 
        fastplay : bool = None, 
        cleanmode : bool = None
    ): 
        """
        Sets the global settings for the application.

        :param fps: The frames per second to set. Must be an integer between 0 and 60.
        :type fps: int, optional
        :param audio: Indicates whether audio should be enabled. Defaults to None.
        :type audio: bool, optional
        :param fastplay: Indicates whether fast play should be enabled. Defaults to None.
        :type fastplay: bool, optional
        :param cleanmode: Indicates whether clean mode should be enabled. Defaults to None.
        :type cleanmode: bool, optional
        :return: The result of the execution of the "globalsetting" command.
        :rtype: str
        """
        args = []
        if fps is not None:
            # 0-60
            if fps < 0 or fps > 60:
                raise ValueError("fps must be between 0 and 60")
            args.append("--fps")
            args.append(str(fps))
        if audio is not None:
            args.append("--audio")
            args.append(str(int(audio)))
        if fastplay is not None:
            args.append("--fastplay")
            args.append(str(int(fastplay)))
        if cleanmode is not None:
            args.append("--cleanmode")
            args.append(str(int(cleanmode)))
        return self.__console.exec("globalsetting", *args)

    def launchex(self, id : typing.Union[str, int], packagename : str): 
        return self.__console.exec("launchex", *self.__resolve_id(id), "--packagename", packagename)

    def operatelist(self, id : typing.Union[str, int]): 
        return self.__console.exec("operatelist", *self.__resolve_id(id))

    def operateinfo(self, id : typing.Union[str, int], file : str): 
        return self.__console.exec("operateinfo", *self.__resolve_id(id), "--file", file)

    def operaterecord(self, id : typing.Union[str, int], content : str): 
        return self.__console.exec("operaterecord", *self.__resolve_id(id), "--content", content)
    
# ANCHOR

    def __getitem__(self, id : typing.Union[str, int]) -> LDConsoleInstance:
        """
        Get an item from the instance dictionary by ID or name.

        Parameters:
            id (Union[str, int]): The ID or name of the item to retrieve.

        Returns:
            Any: The item with the given ID or name.

        Raises:
            KeyError: If no item with the given ID or name exists.
        """
        if len(self.__instances) == 0:
            self.list2()
        for k, v in self.__instances.items():
            if id == k:
                return v
            elif id == v.name:
                return v    
        
        raise KeyError(id)
