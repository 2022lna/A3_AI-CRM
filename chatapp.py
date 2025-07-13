import gradio as gr
from 数据库 import ChatHistoryDB
from 模型回复 import ChatBot
from 异常 import EmptyValueError
from 意图识别 import IntentionRecognizer
from 联网搜索 import TavilySearch
from rag检索 import RAG_QA
choice=IntentionRecognizer()
bot = ChatBot()
db = ChatHistoryDB()
search=TavilySearch()
rag=RAG_QA()
def chatbot_response(user_id,message,chat_history):#message为用户输入的问题内容
    chat_history.append((message, ""))
    yield chat_history, ""
    try:
        if not user_id:
          raise EmptyValueError("用户ID不能为空")
        else:
            if choice.choice_intent(message)=='1':#普通对话
                response = bot.respond(message)
            elif choice.choice_intent(message)=='2':#rag查询文档
                response=rag.query(message)  
            elif choice.choice_intent(message)=='3':#联网查询
                response=search.search_internet(message)
            chat_history[-1]=((message, response))
            db.save_record(user_id,message,response)#保存记录
            yield chat_history,''
    except EmptyValueError:
        chat_history[-1]=((message, "用户ID不能为空，请先输入用户ID!"))
        yield chat_history,''
    
def load_history(user_id,chat_history):
    chat_history.clear()  # 清空当前聊天记录
    record=db.get_records_by_user(user_id)
    try:
        if not record:
          raise EmptyValueError("用户ID不存在")
    except EmptyValueError:
        # chat_history.append((f'加载{user_id}的历史记录', "用户ID不存在"))
        system_msg = "未输入用户ID或该用户ID不存在历史记录"
        chat_history.append((None, system_msg))
        return chat_history
    for row in record:
        chat_history.append((row[2],row[3]))#加载历史记录
    return chat_history
# 创建 Gradio 界面
with gr.Blocks() as chatbot_interface:
    gr.Markdown("# lna的聊天机器人")
    # gr.Markdown("请输入您的问题，右侧可以输入用户ID并加载历史记录")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="对话窗口")
            msg = gr.Textbox(placeholder="请输入您的问题...", label="用户输入")
            clear = gr.Button("清空对话")
        
        with gr.Column(scale=1):
            user_id = gr.Textbox(placeholder="输入用户ID", label="用户ID")
            load = gr.Button("加载历史记录")
    state = gr.State([])
    # 事件绑定
    msg.submit(chatbot_response, [user_id,msg,state], [chatbot,msg])
    clear.click(
        fn=lambda *args: ("", [], []),  # 忽略所有参数，返回清空值
        inputs=None,
        outputs=[msg, chatbot, state],
        queue=False
    )
    load.click(load_history, [user_id,state], outputs=chatbot)

# 启动应用
if __name__ == "__main__":
    chatbot_interface.launch()