import kfp
from kfp import dsl


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
    name='Exit handler',
    description='Exit handler'
)
def ext_handler_pipeline():
    exit_op = print_op('Exit')

    with dsl.ExitHandler(exit_op):
        flip = flip_coin_op()
        print_op(flip.output)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ext_handler_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Exit Handler', __file__ + '.zip')
