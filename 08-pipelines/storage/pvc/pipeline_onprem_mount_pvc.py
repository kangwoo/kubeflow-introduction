import kfp
from kfp import dsl
from kfp import onprem


def pipeline_onprem_mount_pvc():
    pvc_name = "kfp-pvc"
    volume_name = 'pipeline'
    volume_mount_path = '/mnt/pipeline'

    dsl.ContainerOp(
        name='mnist_onprem_mount_pvc',
        image='kangwoo/kfp-mnist-storage:0.0.1',
        arguments=['--model', '/mnt/pipeline/kfp/mnist/model']
    ).apply(onprem.mount_pvc(pvc_name, volume_name=volume_name, volume_mount_path=volume_mount_path))


if __name__ == '__main__':
    my_run = kfp.Client().create_run_from_pipeline_func(pipeline_onprem_mount_pvc, arguments={},
                                                        experiment_name='Storage Experiment')
