import json

metadata = {
    'outputs': [{
        'storage': 'inline',
        'source': '# Inline Markdown\n[A link](https://www.kubeflow.org/)',
        'type': 'markdown',
    }]
}

with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)
