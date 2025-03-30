from typing import AsyncGenerator, Union, Dict, Any
from .model_intent import ModelIntent
from .rule_intent import RuleIntent
import logging
import asyncio


class IntentClassifier(object):
    def __init__(self, intent_config) -> None:
        """
        初始化意图分类器
        :param model_config: 模型分类器配置
        :param rule_config: 规则分类器配置
        """
        model_config = intent_config.get("model_config", {})
        rule_config = intent_config.get("rule_config", {})
        self.model = ModelIntent(**model_config)
        self.rule = RuleIntent(**rule_config)
        self.logger = logging.getLogger(__name__)

    async def work(self, text: str, context: list) -> AsyncGenerator[Dict[str, Union[str, float]], None]:
        """
        异步处理意图分类工作流
        :param text: 输入文本
        :param context: 对话上下文
        :return: 包含意图和置信度的字典
        """
        
        # 使用 gather 并行获取结果
        model_result, rule_result = await asyncio.gather(
            self.model(text, context),
            self.rule(text, context)
        )
        return {
            "intent": rule_result.get("intent") or model_result["intent"],
            "confidence": max(rule_result["confidence"], model_result["confidence"])
        }
        # except Exception as e:
        #     self.logger.error(f"Intent classification failed: {str(e)}")
        #     return {"intent": "error", "confidence": 0.0}

    async def __call__(self, text, context) -> Dict[str, Union[str, float]]:
        """
        调用入口，支持异步生成器
        """
        return await self.work(text, context)
        