import kfp
from kfp import dsl


def webapp_pipeline():
    dsl.ContainerOp(
        name='webapp',
        image='kangwoo/pipeline-webapp:0.0.1',
        output_artifact_paths={'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'}
    )


if __name__ == '__main__':
    arguments = {}
    my_run = kfp.Client().create_run_from_pipeline_func(webapp_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
