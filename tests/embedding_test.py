import requests
import random
import json

query = ["武汉的历史", "给我介绍下武汉"]
data = {"text": query[1]}
while True:
    res = requests.post("http://127.0.0.1:8000/v1/embeddings", data=json.dumps(data))
    print(res)
