import uuid

from kubeflow import fairing
from kubeflow.fairing.kubernetes import utils as k8s_utils

CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'kfserving-tensorflow-train-{uuid.uuid4().hex[:4]}'

command = ["python", "tensorflow_mnist.py", "--model_path", "/mnt/pv/models/tensorflow/mnist"]
output_map = {
    "Dockerfile": "Dockerfile",
    "tensorflow_mnist.py": "tensorflow_mnist.py"
}

fairing.config.set_preprocessor('python', command=command, path_prefix="/app", output_map=output_map)

fairing.config.set_builder('docker', registry=CONTAINER_REGISTRY, image_name="tensorflow-mnist",
                           dockerfile_path="Dockerfile")

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name,
                            pod_spec_mutators=[
                                k8s_utils.mounting_pvc(pvc_name='kfserving-models-pvc', pvc_mount_path='/mnt/pv')],
                            cleanup=True, stream_log=True)

fairing.config.run()
