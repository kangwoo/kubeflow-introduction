import kfp
from kfp import components
from kfp.components import func_to_container_op, InputPath


@func_to_container_op
def print_text(text_path: InputPath()):
    with open(text_path, 'r') as reader:
        for line in reader:
            print(line, end='')


def add(a: float, b: float) -> float:
    return a + b


add_op = components.func_to_container_op(add)


def lightweight_component_pipeline(a='10', b='20'):
    add_task = add_op(a, b)
    print_text(add_task.output)


if __name__ == '__main__':
    arguments = {'a': '1000', 'b': '4'}
    my_run = kfp.Client().create_run_from_pipeline_func(lightweight_component_pipeline, arguments=arguments,
                                                        experiment_name='Sample Experiment')
