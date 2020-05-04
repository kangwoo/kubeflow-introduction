import kfp
from kfp import dsl
from kfp.dsl import PipelineParam


def flip_coin_op():
    return dsl.ContainerOp(
        name='Flip coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import random; result = \'heads\' if random.randint(0,1) == 0 '
                  'else \'tails\'; print(result)" | tee /tmp/output'],
        file_outputs={'output': '/tmp/output'}
    )


def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


@dsl.pipeline(
    name='Pipeline parameters',
    description='Pipeline parameters'
)
def parameters_pipeline(
        predict : str = 'heads'):
    flip = flip_coin_op()
    with dsl.Condition(flip.output == predict):
        print_op('YOU WIN')

    with dsl.Condition(flip.output != predict):
        print_op('YOU LOSE')


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(parameters_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Pipeline parameters', __file__ + '.zip', params={'predict' : 'tails'})