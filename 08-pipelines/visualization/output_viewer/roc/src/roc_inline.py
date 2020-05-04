import json

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve

X, y = make_classification(n_samples=1000, weights=[0.95, 0.05], random_state=5)

model = LogisticRegression().fit(X, y)
y_hat = model.predict(X)

fpr, tpr, thresholds = roc_curve(y, model.decision_function(X))

df_roc = pd.DataFrame({'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds})
csv = df_roc.to_csv(columns=['fpr', 'tpr', 'thresholds'], header=False, index=False)

metadata = {
    'outputs': [{
        'type': 'roc',
        'format': 'csv',
        'schema': [
            {'name': 'fpr', 'type': 'NUMBER'},
            {'name': 'tpr', 'type': 'NUMBER'},
            {'name': 'thresholds', 'type': 'NUMBER'},
        ],
        'source': csv,
        'storage': 'inline',
    }]
}
with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)
