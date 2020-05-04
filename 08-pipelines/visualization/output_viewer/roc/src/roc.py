import json
import os

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve

X, y = make_classification(n_samples=1000, weights=[0.95, 0.05], random_state=5)

model = LogisticRegression().fit(X, y)
y_hat = model.predict(X)

fpr, tpr, thresholds = roc_curve(y, model.decision_function(X))

output = '.'
df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds})
roc_file = os.path.join(output, 'roc.csv')
with open(roc_file, 'w') as f:
    df_roc.to_csv(f, columns=['fpr', 'tpr', 'thresholds'], header=False, index=False)

lines = ''
with open(roc_file, 'r') as f:
    lines = f.read()

metadata = {
    'outputs': [{
        'type': 'roc',
        'format': 'csv',
        'schema': [
            {'name': 'fpr', 'type': 'NUMBER'},
            {'name': 'tpr', 'type': 'NUMBER'},
            {'name': 'thresholds', 'type': 'NUMBER'},
        ],
        'source': lines,
        'storage': 'inline',
    }]
}
with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)