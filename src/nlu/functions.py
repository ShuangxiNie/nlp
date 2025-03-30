import os
import json

def format_case(item):
    context = item["context"]
    query = item["query"]
    nlu = json.dumps(item["nlu"], ensure_ascii=False)
    case_str = f"上下文: {context} \n 用户输入: {query} \n 输出结果: {nlu}"
    return case_str

def load_prompt_examples(filename):
    """
    整理需要加载在 Prompt 中的 case 案例
    """
    results = []
    with open(filename, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            item = json.loads(line) 
            results.append(item)
    return results
            