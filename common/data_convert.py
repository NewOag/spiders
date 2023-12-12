import pandas as pd
import os
import json

if __name__ == '__main__':
    root = "../data/"
    list = os.listdir(root)
    if list is not None and len(list) > 0:
        for file in list:
            if not file.endswith('.json'):
                continue
            with open(root + file, "r") as f:
                list = json.load(f)
                data = {}
                for item in list:
                    for k, v in item.items():
                        if not data.__contains__(k):
                            data[k] = []
                        data[k].append(v)
                df = pd.DataFrame(data)
                df.to_excel("../out/" + file[:-5] + ".xlsx", index=False)
