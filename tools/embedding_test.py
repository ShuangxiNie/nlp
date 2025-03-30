import requests
import random

query = ["武汉的历史", "给我介绍下武汉"]


while True:
    data = {"input": query[1]}
    res = requests.post("http://0.0.0.0:8000/embedding/work", data=data)
    print(res)
