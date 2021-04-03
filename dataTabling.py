import pandas as pd
import json

def getExcel(data, name):
    dataFrame = pd.read_json(json.dumps(data))
    dataFrame.to_excel(f"{name}.xlsx")