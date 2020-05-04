import json

import pandas as pd
from sklearn.metrics import confusion_matrix

y_target = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 2, 2, 0, 2]

vocab = [0, 1, 2]

cm = confusion_matrix(y_target, y_pred, labels=vocab)

data = []
for target_index, target_row in enumerate(cm):
    for predicted_index, count in enumerate(target_row):
        data.append((vocab[target_index], vocab[predicted_index], count))

df_cm = pd.DataFrame(data, columns=['target', 'predicted', 'count'])
csv = df_cm.to_csv(columns=['target', 'predicted', 'count'], header=False, index=False)

metadata = {
    'outputs': [{
        'type': 'confusion_matrix',
        'format': 'csv',
        'schema': [
            {'name': 'target', 'type': 'CATEGORY'},
            {'name': 'predicted', 'type': 'CATEGORY'},
            {'name': 'count', 'type': 'NUMBER'},
        ],
        'source': csv,
        'storage': 'inline',
        'labels': list(map(str, vocab)),
    }]
}

with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)
