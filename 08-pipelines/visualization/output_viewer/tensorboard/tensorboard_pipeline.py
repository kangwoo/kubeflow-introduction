import kfp
from kfp import dsl

from kubernetes.client.models import V1EnvVar


def tensorboard_pipeline(tb_log_dir):
    s3_endpoint = 'minio-service.kubeflow.svc.cluster.local:9000'
    minio_endpoint = "http://" + s3_endpoint
    minio_username = "minio"
    minio_key = "minio123"
    minio_region = "us-east-1"

    dsl.ContainerOp(
        name='tensorboard',
        image='kangwoo/kfp-tensorboard:0.0.1',
        arguments=['--tb_log_dir', tb_log_dir],
        output_artifact_paths={'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'}
    ).add_env_variable(V1EnvVar(name='S3_ENDPOINT', value=s3_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ENDPOINT_URL', value=minio_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value=minio_username)) \
        .add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value=minio_key)) \
        .add_env_variable(V1EnvVar(name='AWS_REGION', value=minio_region)) \
        .add_env_variable(V1EnvVar(name='S3_USE_HTTPS', value='0')) \
        .add_env_variable(V1EnvVar(name='S3_VERIFY_SSL', value='0'))


if __name__ == '__main__':
    arguments = {'tb_log_dir': 's3://tensorboard/mnist'}
    my_run = kfp.Client().create_run_from_pipeline_func(tensorboard_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
