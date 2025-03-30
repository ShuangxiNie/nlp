import json
from collections import Counter
import pandas as pd

def load_ds_data(fin, fout):
    """
        从对话日志中获取用户 Query
    """
    total_query_list = []
    with open(fin, 'r') as f:
        for idx, ds in enumerate(f.readlines()):
            items = json.loads(ds)
            user_query_list = [x["content"] for x in items if x["role"]=="user"]
            total_query_list.extend(user_query_list)
    
    query2num = Counter(total_query_list)

    df = pd.DataFrame(query2num.most_common(), columns=["query", 'count'])
    df.to_excel(fout, index=False)
    

if __name__ == "__main__":

    fin = "train_data/dialogue_data.txt"
    fout = "train_data/query_count.xlsx"
    load_ds_data(fin, fout)