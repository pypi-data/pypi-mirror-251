import inspect
from functools import wraps

def method_callback_decorator(method):
    if not hasattr(method, '_callbacks'):
        method._callbacks = []
        method._callback_params = []

    @wraps(method)
    def wrapped(instance, *args, **kwargs):
        result = method(instance, *args, **kwargs)
        trigger_callbacks(instance, result, *args, **kwargs)
        return result

    def register_callback(func):
        if func in method._callbacks:
            return
        params = inspect.signature(func).parameters
        param_keys = list(params.keys())
        method._callbacks.append(func)
        method._callback_params.append(param_keys)

    def remove_callback(func):
        if func not in method._callbacks:
            return
        index = method._callbacks.index(func)
        method._callbacks.pop(index)
        method._callback_params.pop(index)

    def trigger_callbacks(instance, result, *args, **kwargs):
        for callback, param_keys in zip(method._callbacks, method._callback_params):
            params = {k: v for k, v in kwargs.items() if k in param_keys}
            if "result" in param_keys:
                params["result"] = result
            if "instance" in param_keys:
                params["instance"] = instance
            if "args" in param_keys:
                params["args"] = args
            if "kwargs" in param_keys:
                params["kwargs"] = kwargs
            callback(**params)

    wrapped.register_callback = register_callback
    wrapped.remove_callback = remove_callback

    return wrapped