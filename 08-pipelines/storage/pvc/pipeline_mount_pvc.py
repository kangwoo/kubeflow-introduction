import kfp
from kfp import dsl

from kubernetes.client.models import V1PersistentVolumeClaimVolumeSource, \
    V1Volume, V1VolumeMount


def pipeline_mount_pvc():
    pvc_name = "kfp-pvc"
    volume_name = 'pipeline'
    volume_mount_path = '/mnt/pipeline'

    dsl.ContainerOp(
        name='mnist_pvc',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', '/mnt/pipeline/kfp/mnist/model']
    ).add_volume(V1Volume(name=volume_name, persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(claim_name=pvc_name))) \
        .add_volume_mount(V1VolumeMount(mount_path=volume_mount_path, name=volume_name))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_mount_pvc, arguments={},
                                                        experiment_name='Storage Experiment')