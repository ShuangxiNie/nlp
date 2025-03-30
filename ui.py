from openai import OpenAI
import gradio as gr
from utils.config_loader import load_config

nlu_config = load_config("./configs/nlu.yaml")

api_key = nlu_config.get("api_key")
base_url = nlu_config.get("base_url")

client = OpenAI(api_key=api_key,  base_url=base_url)

# system_prompt = "你是ARA的问答助手; 结合上下文，回复用户的问题; \n"
system_prompt = "</think>"

# 提取常量
MODEL_NAME = 'Qwen/QwQ-32B'
MAX_HISTORY = 3

def format_history(history):
    """格式化历史记录"""
    history_openai_format = []
    for human, assistant in history[-MAX_HISTORY:]:
        history_openai_format.extend([
            {"role": "user", "content": human},
            {"role": "assistant", "content": assistant}
        ])
    
    return history_openai_format

def predict(message, history):
    try:
        # 格式化历史记录
        history_openai_format = format_history(history)
        history_openai_format.append({"role": "user", "content": message + system_prompt})
        
        # 获取模型响应
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history_openai_format,
            temperature=1.0,
            stream=True
        )

        # 流式处理响应
        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.reasoning_content:
                partial_message += chunk.choices[0].delta.reasoning_content
                yield partial_message
            if chunk.choices[0].delta.content:
                partial_message += chunk.choices[0].delta.content
                yield partial_message
                
    except Exception as e:
        yield f"发生错误: {str(e)}"




def predict(message, history, llm_name):
    history_openai_format = []
    for human, assistant in history[-3:]:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message + system_prompt})
  
    response = client.chat.completions.create(model=llm_name,
    messages= history_openai_format,
    temperature=1.0,
    stream=True)

    partial_message = ""
    for chunk in response:
        
        # 输出思考过程
        if chunk.choices[0].delta.reasoning_content is not None:
             partial_message = partial_message + chunk.choices[0].delta.reasoning_content
             yield partial_message
        
        # 输出答案 
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message

# 创建统一的ChatInterface配置
def chat_interface(llm_name):
    return gr.ChatInterface(
        fn=predict,
        additional_inputs=llm_name,
        fill_height=True,
        fill_width=True
        ).queue(default_concurrency_limit=5)

# 创建TabbedInterface
app = gr.TabbedInterface(
    [chat_interface("Qwen/QwQ-32B"), chat_interface("Qwen/QwQ-32B")],
    ["DeepSeek满血版", "DeepSeek简化版"]
)

app.launch(debug=True)
