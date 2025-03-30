import gradio as gr

# 定义第一个聊天机器人的响应函数
def chatbot1(message):
    return f"Chatbot1: {message}"

# 定义第二个聊天机器人的响应函数
def chatbot2(message):
    return f"Chatbot2: {message}"

# 创建第一个聊天机器人的Gradio接口
chatbot1_interface = gr.Interface(
    fn=chatbot1,
    inputs=gr.inputs.Textbox(lines=2, placeholder="Enter your message here..."),
    outputs="text",
    title="Chatbot 1",
    description="This is the first chatbot"
)

# 创建第二个聊天机器人的Gradio接口
chatbot2_interface = gr.Interface(
    fn=chatbot2,
    inputs=gr.inputs.Textbox(lines=2, placeholder="Enter your message here..."),
    outputs="text",
    title="Chatbot 2",
    description="This is the second chatbot"
)

# 将两个聊天机器人接口放置在同一个页面上
app = gr.TabbedInterface([chatbot1_interface, chatbot2_interface], ["Chatbot 1", "Chatbot 2"])

# 启动Gradio应用
if __name__ == "__main__":
    app.launch()