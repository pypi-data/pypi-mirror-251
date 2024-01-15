
import datetime
import typing
from pyldplayer._utils.misc import hasAndEqual
from pyldplayer.consoleProc import LDConsoleProc


class LDConsoleProcCache:
    class Default:
        exec_history : typing.ClassVar[bool] = True
        query_history : typing.ClassVar[bool] = True
        max_exec : typing.ClassVar[int] = 50
        max_query : typing.ClassVar[int] = 50
    
    def __init__(
        self, 
        proc : LDConsoleProc
    ):
        super().__init__()
        self.__proc = proc
        self.exec_history = self.Default.exec_history
        self.query_history = self.Default.query_history
        self.max_exec = self.Default.max_exec
        self.max_query = self.Default.max_query
    
    @property
    def query_history(self):
        return self.__query_history
    
    @query_history.setter
    def query_history(self, value : bool):
        if hasAndEqual(self, "__query_history", value):
            return
        
        self.__query_history_data = []
        self.__query_history = value
        if value:
            self.__proc.query.register_callback(self.__query_history_callback)
        else:
            self.__proc.query.remove_callback(self.__query_history_callback)
        
    def __query_history_callback(self, result, args):
        timestamp = datetime.datetime.now()
        self.__query_history_data.append((timestamp, args, result))
        if len(self.__query_history_data) > self.max_query:
            self.__query_history_data.pop(0)
    
    @property
    def exec_history(self):
        return self.__exec_history
    
    @exec_history.setter
    def exec_history(self, value : bool):
        if hasAndEqual(self, "__exec_history", value):
            return
        
        self.__exec_history_data = []
        self.__exec_history = value
        if value:
            self.__proc.exec.register_callback(self.__exec_history_callback)
        else:
            self.__proc.exec.remove_callback(self.__exec_history_callback)
        
    def __exec_history_callback(self, result, args):
        timestamp = datetime.datetime.now()
        self.__exec_history_data.append((timestamp, args, result))
        if len(self.__exec_history_data) > self.max_exec:
            self.__exec_history_data.pop(0)
            
    @property
    def queryLast(self) -> typing.Tuple[datetime.datetime, tuple, str]:
        if len(self.__query_history_data) == 0:
            return None
        return self.__query_history_data[-1]
    
    @property
    def execLast(self) -> typing.Tuple[datetime.datetime, tuple, str]:
        if len(self.__exec_history_data) == 0:
            return None
        return self.__exec_history_data[-1]

    def getLastResult(self, cmd : list, flag : typing.Literal["both", "query", "exec"]):
        cmdTuple = tuple(cmd)
        if flag in ["both", "query"]:
            for data in self.__query_history_data:
                if data[1] == cmdTuple:
                    return data
                
        if flag in ["both", "exec"]:
            for data in self.__exec_history_data:
                if data[1] == cmdTuple:
                    return data
                
        return None
    
    