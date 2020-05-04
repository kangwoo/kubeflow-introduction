import kfp
from kfp import dsl


def confusion_matrix_pipeline():
    dsl.ContainerOp(
        name='confusion-matrix',
        image='kangwoo/pipeline-confusion-matrix:0.0.1',
        output_artifact_paths={'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'}
    )


if __name__ == '__main__':
    arguments = {}
    my_run = kfp.Client().create_run_from_pipeline_func(confusion_matrix_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
