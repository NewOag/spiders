import pandas as pd
import os
import json

if __name__ == '__main__':
    root = "../data/"
    li = os.listdir(root)
    out = "../out/"
    if not os.path.isdir(out):
        os.mkdir(out)

    if li is not None and len(li) > 0:
        for file in li:
            if not file.endswith('.json'):
                continue
            with open(root + file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                data = {}
                for item in raw_data:
                    for k, v in item.items():
                        if not data.__contains__(k):
                            data[k] = []
                        data[k].append(v)
                df = pd.DataFrame(data)
                df.to_excel("../out/" + file[:-5] + ".xlsx", index=False)
