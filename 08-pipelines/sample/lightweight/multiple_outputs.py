from typing import NamedTuple

import kfp
import kfp.components as comp
from kfp import dsl


def print_op(msg):
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


def add_multiply_two_numbers(a: float, b: float) \
        -> NamedTuple('Outputs', [('sum', float), ('product', float)]):
    return (a + b, a * b)


add_multiply_two_numbers_op = comp.func_to_container_op(add_multiply_two_numbers)


@dsl.pipeline(
    name='Multiple outputs pipeline',
    description='A pipeline to showcase multiple outputs.'
)
def multiple_outputs_pipeline(a='10', b='20'):
    add_multiply_task = add_multiply_two_numbers_op(a, b)
    print_op('sum={}, product={}'.format(add_multiply_task.outputs['sum'],
                                         add_multiply_task.outputs['product']))


if __name__ == '__main__':
    arguments = {'a': '3', 'b': '4'}
    my_run = kfp.Client().create_run_from_pipeline_func(multiple_outputs_pipeline,
                                                        arguments=arguments, experiment_name='Sample Experiment')
