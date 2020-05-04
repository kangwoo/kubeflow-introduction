import kfp
from kfp import aws
from kfp import dsl


def pipeline_use_aws_secret():
    secret_name = "kfp-aws-secret"

    dsl.ContainerOp(
        name='mnist_use_aws_secret',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', 's3://tensorflow/kfp/mnist/model']
    ).apply(aws.use_aws_secret(secret_name,
                               aws_access_key_id_name='AWS_ACCESS_KEY_ID',
                               aws_secret_access_key_name='AWS_SECRET_ACCESS_KEY'))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_use_aws_secret, arguments={},
                                                        experiment_name='Storage Experiment')