import json
import os

import pandas as pd
from sklearn.metrics import classification_report

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [0, 1, 1, 0, 0, 1]

target_names = ['class 0', 'class 1']
report = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)
print(report)

df_report = pd.DataFrame(report).transpose()

output = '.'
table_file = os.path.join(output, 'table.csv')
with open(table_file, 'w') as f:
    df_report.to_csv(f, header=False)

lines = ''
with open(table_file, 'r') as f:
    lines = f.read()

metadata = {
    'outputs': [{
        'type': 'table',
        'format': 'csv',
        'header': [''] + [x for x in df_report],
        'source': lines,
        'storage': 'inline',
    }]
}

with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)