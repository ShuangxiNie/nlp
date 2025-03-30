import pandas as pd
import json


def read_dialogue_data(filename):
    """
    读取 excel 中的 历史对话数据
    """

    df = pd.read_excel(filename)

    df = df[["会话编号", "消息编号", "消息内容", "发送者姓名", "发送时间"]]
    df.columns = ["session_id", "message_id", "content", "sender", "time"]
    df["role"] = df["sender"].apply(lambda x: "system" if x=="超级管理员" else "user")
    
    das = df.groupby("session_id")

    results = []
    for da_id, group in das:
        sorted_group = group.sort_values(by="message_id", ascending=True)

        messages_list = sorted_group.to_dict('records')

        results.append(json.dumps(messages_list, ensure_ascii=False))

    return results



if __name__ == "__main__":

    """
        提取对话数据
    """
    
    fin1 = "raw_data/副本武汉.xlsx"
    fin2 = "raw_data/副本长沙.xlsx"

    wuhan_data = read_dialogue_data(fin1) 
    changsha_data = read_dialogue_data(fin2)
    data = wuhan_data + changsha_data

    fout = "train_data/dialogue_data.txt"

    with open(fout, 'w') as f:
        f.write("\n".join(data))

        

        

