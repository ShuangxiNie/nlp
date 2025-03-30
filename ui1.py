import gradio as gr
import asyncio
from openai import OpenAI
from utils.config_loader import load_config

nlu_config = load_config("./configs/nlu.yaml")

api_key = nlu_config.get("api_key")
base_url = nlu_config.get("base_url")

client = OpenAI(api_key=api_key,  base_url=base_url)

# system_prompt = "你是ARA的问答助手; 结合上下文，回复用户的问题; \n"
system_prompt = "</think>"

def predict(message, history):
    history_openai_format = []
    for human, assistant in history[-3:]:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message + system_prompt})
  
    response = client.chat.completions.create(model='Qwen/QwQ-32B',
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


with gr.Blocks() as interface:
     
    chatbot = gr.Chatbot(label="对话历史")

    with gr.Row():
         query = gr.Textbox(label="输入", show_label=True)
    
    query.submit(predict, inputs=query, outputs=chatbot)

interface.launch()