import requests

local_server = "http://localhost:8000"


def test_hello():
    response = requests.get(local_server + "/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_analyze():
    response = requests.post(local_server + "/analyze", json={"query": "你们能拍什么风格的照片"})
    assert response.json()["intent"] == "询问风格"

    response = requests.post(local_server + "/analyze", json={"query": "你们有样例照片吗"})
    assert response.json()["intent"] == "询问客照样照"

    # response = requests.post(local_server + "/analyze", json={"query": "什么时间可以拍啊"})
    # assert response.json()["intent"] == "询问时间"

    # response = requests.post(local_server + "/analyze", json={"query": "大概要多少钱"})
    # assert response.json()["intent"] == "询问价格"

    # response = requests.post(local_server + "/analyze", json={"query": "现在有活动吗, 介绍下"})
    # assert response.json()["intent"] == "询问活动详情"

    # response = requests.post(local_server + "/analyze", json={"query": "你们在哪里"})
    # assert response.json()["intent"] == "询问地址"

    # response = requests.post(local_server + "/analyze", json={"query": "都有什么类型"})
    # assert response.json()["intent"] == "询问拍照类型"

    # response = requests.post(local_server + "/analyze", json={"query": "可以"})
    # assert response.json()["intent"] == "有意向"

    # response = requests.post(local_server + "/analyze", json={"query": "我加你v"})
    # assert response.json()["intent"] == "主动要微信"

    # response = requests.post(local_server + "/analyze", json={"query": "武汉"})
    # assert response.json()["intent"] == "回答地区"

    # response = requests.post(local_server + "/analyze", json={"query": "是的，要结婚了"})
    # assert response.json()["intent"] == "回答需求"

    # response = requests.post(local_server + "/analyze", json={"query": "不用了"})
    # assert response.json()["intent"] == "考虑/了解/不需要"

    # response = requests.post(local_server + "/analyze", json={"query": "别烦我"})
    # assert response.json()["intent"] == "别打电话"

    # response = requests.post(local_server + "/analyze", json={"query": "就在这聊"})
    # assert response.json()["intent"] == "不给联系方式"

    # response = requests.post(local_server + "/analyze", json={"query": ""})
    # assert response.json()["intent"] == "售后"

    # response = requests.post(local_server + "/analyze", json={"query": ""})
    # assert response.json()["intent"] == "停止发送"

    # response = requests.post(local_server + "/analyze", json={"query": ""})
    # assert response.json()["intent"] == "收到联系方式"

    # response = requests.post(local_server + "/analyze", json={"query": ""})
    # assert response.json()["intent"] == "收到空号"


def main():
    test_analyze()

if __name__ == "__main__":
    main()
