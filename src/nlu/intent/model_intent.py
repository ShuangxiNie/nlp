from .base import BaseIntent

class ModelIntent(BaseIntent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = kwargs.get("model")
    
    async def work(self, text, context):
        return {"intent": "unknown", "confidence": 0.0}
    