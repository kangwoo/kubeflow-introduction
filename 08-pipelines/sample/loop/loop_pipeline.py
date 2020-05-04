import kfp
from kfp import dsl


def flip_coins_op():
    return dsl.ContainerOp(
        name='Flip coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import json; import sys; import random; '
                   'json.dump([(\'heads\' if random.randint(0,1) == 1 else \'tails\') for i in range(10)], '
                   'open(\'/tmp/output.json\', \'w\'))"'],
        file_outputs={'output': '/tmp/output.json'}
    )


def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


@dsl.pipeline(
    name='Loop pipeline',
    description='Loop pipeline'
)
def loop_pipeline():
    flips = flip_coins_op()
    with dsl.ParallelFor(flips.output) as item:
        print_op(item)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(loop_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Loop pipeline', __file__ + '.zip')
