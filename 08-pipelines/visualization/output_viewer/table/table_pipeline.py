import kfp
from kfp import dsl


def table_pipeline():
    dsl.ContainerOp(
        name='table',
        image='kangwoo/pipeline-table:0.0.1',
        output_artifact_paths={'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'}
    )


if __name__ == '__main__':
    arguments = {}
    my_run = kfp.Client().create_run_from_pipeline_func(table_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
