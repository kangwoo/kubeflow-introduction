import os

import kfp
from kfp import dsl


def number_op():
    return dsl.ContainerOp(
        name='Generate numbers',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "print(\'1\\n2\\n3\\n4\\n5\\n6\\n7\\n8\\n9\\n10\')" | tee /tmp/output'],
        file_outputs={'output': '/tmp/output'}
    )


def print_op(msg):
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


component_root = './components/sample/multiply'
multiply_op = kfp.components.load_component_from_file(os.path.join(component_root, 'component.yaml'))
# multiply_op = kfp.components.load_component_from_url('http://....../component.yaml')


@dsl.pipeline(
    name='Multiply component pipeline',
    description='Multiply component pipeline'
)
def multiply_pipeline():
    numbers = number_op()
    multiply_task = multiply_op(
        input_1=numbers.output,
        parameter_1='6',
    )
    print_op(multiply_task.outputs['output_1'])


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(multiply_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Component Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Multiply pipeline', __file__ + '.zip')
