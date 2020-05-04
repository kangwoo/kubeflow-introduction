import kfp
from kfp import dsl
from kfp import gcp


def pipeline_use_gcp_secret():
    secret_name = 'user-gcp-sa'

    dsl.ContainerOp(
        name='mnist_use_gcp_secret',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', 'gs://kfp-bucket/kfp/mnist/model']
    ).apply(gcp.use_gcp_secret(secret_name))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_use_gcp_secret, arguments={},
                                                        experiment_name='Storage Experiment')
