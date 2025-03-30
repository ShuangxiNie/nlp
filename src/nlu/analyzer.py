from abc import ABC, abstractmethod
import openai
import logging
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional
import json
import os
from .intent import IntentClassifier
from .slot import SlotExtractor
from .functions import load_prompt_examples, format_case


# 基类
class BaseAnalyzer(ABC):

    @abstractmethod    
    async def work(self, data):
        raise NotImplementedError
    
    async def __call__(self, data):
        return await self.work(data)
    
# 定义响应模型（根据NLU需求调整）
class NLUResult(BaseModel):
    intent: str
    confidence: Optional[float] = 1.0
    entities: Optional[List[Dict[str, str]]] = []
    sentiment: Optional[str] = "neutral"

class LLMAnalyzer(BaseAnalyzer):
    def __init__(self, **kwargs) -> None:
        
        base_url = kwargs.get("base_url")
        api_key = kwargs.get("api_key")
        self.model = kwargs.get("llm_model")

        self.client = OpenAI(api_key=api_key,  base_url=base_url)
        
        intents = kwargs.get("intents")
        self.intent_num = len(intents)
        self.intent_str = ",".join(intents)

        # prompt 设计
        prompt_examples_file = kwargs.get("prompt_examples_file")
        self.prompt_examples = load_prompt_examples(prompt_examples_file)
         
        self.nlu_prompt = self.make_prompt()
        # print(f"nlu_prompt: {self.nlu_prompt}")

    
    def make_prompt(self):
        """
            生成prompt; # TODO, 动态生成 prompt 
        """

        tmp = []
        for idx, case in enumerate(self.prompt_examples):
            tmp.append(f"example{idx+1}:" + format_case(case))

        cases_str = "\n".join(tmp)

        nlu_prompt = f'''
            ### 任务
            1. 请根据给定的上下文信息和用户当前输入, 对用户的意图进行分析
            2. 用户的意图共有 {self.intent_num} 种，分别是 {self.intent_str}
            3. 以 json 格式输出, 意图用 intent 字段表示
            ### 例子
            {cases_str}
        '''

        return nlu_prompt

    async def work(self, data: str):
        """Use LLM for natural language understanding"""

        query = data["query"]
        context = data.get("context", "")
        model = data.get("model", self.model)
        
        # 创建聊天补全
        response = self.client.chat.completions.create(
            model= model,  # 指定模型
            messages=[
                {"role": "system", "content": self.nlu_prompt},
                {"role": "user", "content": f"上下文信息：{context} \n 用户当前输入: {query}"}
            ],
            temperature=0.1,
            max_tokens=1024
        )
        
        # 对大模型的结果做后处理
        nlu_result = self.post_process(response)

        return nlu_result.model_dump()


    # 在原有代码后添加处理逻辑
    def post_process(self, response):
        try:
            # 提取模型返回内容
            content = response.choices[0].message.content
            
            # 安全解析（限制最大长度）
            if len(content) > 2048:
                raise ValueError("Response content too long")
                
            # 尝试解析JSON（处理大模型常见的格式问题）
            parsed = json.loads(
                content.strip("`").replace("json", "", 1),  # 处理可能的Markdown代码块
                strict=False  # 允许特殊字符
            )
            
            # 数据验证
            validated = NLUResult(**parsed)

            # 后处理
            validated.intent = validated.intent.lower().strip()  # 统一小写
            validated.confidence = round(validated.confidence, 2)  # 保留两位小数
            
            # 过滤空实体
            validated.entities = [
                {k: v.strip() for k, v in e.items() if v}
                for e in validated.entities
            ]
            
            return validated
            
        except (IndexError, AttributeError) as e:
            logging.error(f"Invalid API response structure: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e.msg} at line {e.lineno}")
            logging.debug(f"Raw content: {content}")  # 记录原始响应
            return None
        except ValidationError as e:
            logging.error(f"Validation error: {str(e)}")
            logging.debug(f"Raw parsed: {parsed}")  # 记录解析后的原始数据
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None



class DQUAnalyzer(BaseAnalyzer):
    def __init__(self, **kwargs) -> None:

        intent_config = kwargs.get("intent_config", {})
        slot_config = kwargs.get("slot_config", {})
        
        self.intent_worker = IntentClassifier(intent_config)
        self.slot_worker = SlotExtractor(slot_config)  # 补全缺失的初始化
        
    async def work(self, data: str):
        """Traditional pipeline processing"""
        query = data.get("query", "")
        context = data.get("context", [])
        
        # 意图识别
        intent = await self.intent_worker(query, context)
        
        # 槽位识别, TODO
        # slots = await self.slot_worker(data)
        return {"intent": intent, "slots": {}}


class NLUAnalyzer(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        use_llm = kwargs.get("use_llm", False)
        self.analyzer = (LLMAnalyzer(**kwargs) if use_llm else DQUAnalyzer(**kwargs))

    async def analyze(self, data: str) -> dict:
        """Main entry point for NLU processing"""
        return await self.analyzer(data)
