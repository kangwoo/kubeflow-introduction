import os

import kfp
from kfp import dsl
from kubernetes.client.models import V1EnvVar, V1VolumeMount, V1Volume, \
    V1SecretVolumeSource


def pipeline_gcs():
    GCSCredentialFileName = "user-gcp-sa.json"
    GCSCredentialVolumeName = "user-gcp-sa"
    GCSCredentialVolumeMountPath = "/var/secrets/"
    GCSCredentialEnvKey = "GOOGLE_APPLICATION_CREDENTIALS"
    GCSCredentialFilePath = os.path.join(GCSCredentialVolumeMountPath, GCSCredentialFileName)

    secret_name = 'user-gcp-sa'

    dsl.ContainerOp(
        name='mnist-gcs',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', 'gs://kfp-bucket/kfp/mnist/model']
    ).add_volume(V1Volume(name=GCSCredentialVolumeName, secret=V1SecretVolumeSource(secret_name=secret_name))) \
        .add_volume_mount(V1VolumeMount(name=GCSCredentialVolumeName, mount_path=GCSCredentialVolumeMountPath)) \
        .add_env_variable(V1EnvVar(name=GCSCredentialEnvKey, value=GCSCredentialFilePath))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_gcs, arguments={},
                                                        experiment_name='Storage Experiment')
