import kfp
from kfp import dsl

from kubernetes.client.models import V1EnvVar, V1EnvVarSource, V1SecretKeySelector


def pipeline_s3():
    secret_name = "kfp-aws-secret"

    s3_endpoint = 'minio-service.kubeflow.svc.cluster.local:9000'
    minio_endpoint = "http://" + s3_endpoint
    minio_region = "us-east-1"

    dsl.ContainerOp(
        name='mnist-s3',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', 's3://tensorflow/kfp/mnist/model']
    ).add_env_variable(V1EnvVar(name='S3_ENDPOINT', value=s3_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ENDPOINT_URL', value=minio_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID',
                                   value_from=V1EnvVarSource(
                                       secret_key_ref=V1SecretKeySelector(name=secret_name, key='AWS_ACCESS_KEY_ID')))) \
        .add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY',
                                   value_from=V1EnvVarSource(secret_key_ref=V1SecretKeySelector(name=secret_name,
                                                                                                key='AWS_SECRET_ACCESS_KEY')))) \
        .add_env_variable(V1EnvVar(name='AWS_REGION', value=minio_region)) \
        .add_env_variable(V1EnvVar(name='S3_USE_HTTPS', value='0')) \
        .add_env_variable(V1EnvVar(name='S3_VERIFY_SSL', value='0'))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_s3, arguments={},
                                                        experiment_name='Storage Experiment')
