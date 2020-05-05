import uuid
from kubeflow import fairing
from kubeflow.fairing.kubernetes import utils as k8s_utils

CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'kfserving-sklearn-train-{uuid.uuid4().hex[:4]}'

command=["python", "iris.py", "--model_path", "/mnt/pv/models/sklearn/iris"]
output_map = {
    "Dockerfile": "Dockerfile",
    "iris.py": "iris.py"
}

fairing.config.set_preprocessor('python', command=command, path_prefix="/app", output_map=output_map)

fairing.config.set_builder('docker', registry=CONTAINER_REGISTRY, image_name="sklean-iris", dockerfile_path="Dockerfile")

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name,
                            pod_spec_mutators=[k8s_utils.mounting_pvc(pvc_name='kfserving-models-pvc', pvc_mount_path='/mnt/pv')],
                            cleanup=False, stream_log=True)

fairing.config.run()