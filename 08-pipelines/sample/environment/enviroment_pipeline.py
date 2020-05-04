import kfp

import kfp.dsl as dsl
from kubernetes.client.models import V1EnvVar


def print_env_op():
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['sh', '-c', 'echo $example_env'],
    )


@dsl.pipeline(
    name='Environment pipeline',
    description='Environment pipeline'
)
def environment_pipeline():
    env_var = V1EnvVar(name='example_env', value='env_variable')

    print_env_op().add_env_variable(env_var)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(environment_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Environment pipeline', __file__ + '.zip')
