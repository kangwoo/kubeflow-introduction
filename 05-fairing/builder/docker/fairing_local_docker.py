import uuid

from kubeflow import fairing

CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'fairing-python-docker-job-{uuid.uuid4().hex[:4]}'

command = ["python", "tensorflow_mnist.py"]
output_map = {
    "Dockerfile": "Dockerfile",
    "tensorflow_mnist.py": "tensorflow_mnist.py"
}

fairing.config.set_preprocessor('python', command=command, path_prefix="/app", output_map=output_map)

fairing.config.set_builder('docker', registry=CONTAINER_REGISTRY, image_name="fairing-python-docker-job",
                           dockerfile_path="Dockerfile")

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True)

fairing.config.run()
