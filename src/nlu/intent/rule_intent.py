from .base import BaseIntent

class RuleIntent(BaseIntent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def work(self, text, context):
        return {"intent": "unknown"}