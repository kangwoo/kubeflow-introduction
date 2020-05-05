import uuid

import s3_utils

from kubeflow import fairing
from kubeflow.fairing.kubernetes import utils as k8s_utils



CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'tensorflow-mnist-s3-job-{uuid.uuid4().hex[:4]}'

command = ["python", "tensorflow_mnist.py", "--model_path", "s3://tensorflow/mnist/model"]
output_map = {
    "Dockerfile": "Dockerfile",
    "tensorflow_mnist.py": "tensorflow_mnist.py"
}
fairing.config.set_preprocessor('python', command=command, path_prefix="/app", output_map=output_map)

fairing.config.set_builder('docker', registry=CONTAINER_REGISTRY, image_name="tensorflow-mnist",
                           dockerfile_path="Dockerfile")

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name,
                            pod_spec_mutators=[
                                s3_utils.aws_credentials(secret_name='s3-secret')
                            ],
                            cleanup=False, stream_log=True)

fairing.config.run()
