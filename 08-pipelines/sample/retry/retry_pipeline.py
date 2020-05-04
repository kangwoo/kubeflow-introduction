import kfp
from kfp import dsl


def random_exit_op(exit_codes):
    return dsl.ContainerOp(
        name='random_failure',
        image='python:alpine3.6',
        command=['python', '-c'],
        arguments=[
            'import random; import sys; exit_code = int(random.choice(sys.argv[1].split(","))); print(exit_code); sys.exit(exit_code)',
            exit_codes]
    )


@dsl.pipeline(
    name='Retry pipeline',
    description='Retry pipeline'
)
def retry_pipeline():
    random_exit_op('0,1,2,3').set_retry(10)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(retry_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Retry pipeline', __file__ + '.zip')
