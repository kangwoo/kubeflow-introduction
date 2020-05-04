from typing import NamedTuple

import kfp
from kfp.components import func_to_container_op


@func_to_container_op
def train() -> \
        NamedTuple('output', [('mlpipeline_metrics', 'metrics')]):
    import json
    loss = 0.812345
    accuracy = 0.9712345
    metrics = {
        'metrics': [{
            'name': 'accuracy',
            'numberValue': float(accuracy),
            'format': "PERCENTAGE",
        }, {
            'name': 'loss',
            'numberValue': float(loss),
            'format': "RAW",
        }]
    }
    from collections import namedtuple

    output = namedtuple('output', ['mlpipeline_metrics'])
    return output(json.dumps(metrics))


def lightweight_metrics_pipeline():
    train()


if __name__ == '__main__':
    arguments = {}
    my_run = kfp.Client().create_run_from_pipeline_func(lightweight_metrics_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
