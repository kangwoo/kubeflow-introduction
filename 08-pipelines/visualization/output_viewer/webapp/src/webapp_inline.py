import json

metadata = {
    'outputs': [{
        'type': 'web-app',
        'storage': 'inline',
        'source': '<p><strong>Kubeflow pipelines</strong> are reusable end-to-end ML workflows built using the Kubeflow Pipelines SDK.</p>',
    }]
}

with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)
