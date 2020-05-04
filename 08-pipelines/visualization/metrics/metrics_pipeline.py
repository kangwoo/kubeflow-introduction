import kfp
from kfp import dsl


@dsl.pipeline(
    name='Metrics pipeline',
    description='Metrics pipeline'
)
def metrics_pipeline():
    dsl.ContainerOp(
        name='mnist-kfp-metrics',
        image='kangwoo/pipeline-metrics:0.0.1',
        output_artifact_paths={'mlpipeline-metrics': '/mlpipeline-metrics.json'}
    )


if __name__ == '__main__':
    arguments = {}
    my_run = kfp.Client().create_run_from_pipeline_func(metrics_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
