import kfp
from kfp import dsl


@kfp.dsl.component
def train_component_op():
    return kfp.dsl.ContainerOp(
        name='train',
        image='kangwoo/pipelines-tensorflow-mnist:0.0.1'
    )


@dsl.pipeline(
    name='My pipeline',
    description='My pipeline'
)
def my_pipeline():
    train_task = train_component_op()


if __name__ == '__main__':
    # Compile
    pipeline_package_path = 'my_pipeline.zip'
    kfp.compiler.Compiler().compile(my_pipeline, pipeline_package_path)

    # Run
    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'my_pipeline', pipeline_package_path)