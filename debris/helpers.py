def call(_callable, *args, **kwargs):
    return _callable(*args, **kwargs) if hasattr(_callable, "__call__") else _callable

def callattr(cls, attr, *args, **kwargs):
    if attr:
        if hasattr(cls, attr):
            return getattr(cls, attr)(*args, **kwargs)
        elif hasattr(attr, "__call__"):
            return attr(*args, **kwargs)
