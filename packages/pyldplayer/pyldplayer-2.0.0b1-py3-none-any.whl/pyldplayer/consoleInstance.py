from pyldplayer._internal._interfaces.ldconsoleI import LDConsoleI
from dataclasses import dataclass, field
from pyldplayer._internal._interfaces.ldconsoleInstanceI import LDConsoleInstanceI, availableMethod
import typing

@dataclass(frozen=True)
class LDConsoleInstance(LDConsoleInstanceI):
    id : int
    name : str
    top_window_handle : int 
    bind_window_handle : int
    android_started_int : int
    pid : int
    pid_of_vbox : int
    
    _console : LDConsoleI
    _others : typing.Dict[str, object] = field(default_factory=dict)
    
    def __repr__(self) -> str:
        return f"LDConsoleInstance<{self.name}>"
    
    def __post_init__(self):
        self._attach_methods()
    
    def _attach_methods(self):
        for method_name in availableMethod:
            if hasattr(self._console, method_name):
                bound_method = self._create_bound_method(method_name)
                object.__setattr__(self, method_name, bound_method)

    def _create_bound_method(self, method_name):
        def bound_method(*args, **kwargs):
            method = getattr(self._console, method_name)
            return method(self.id, *args, **kwargs)
        return bound_method