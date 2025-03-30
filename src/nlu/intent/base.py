from typing import Any


class BaseIntent:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
    
    def work(self, text, context):
        raise NotImplementedError("Subclasses must implement this method")
    

    def __call__(self, text, context) -> Any:
        return self.work(text, context)