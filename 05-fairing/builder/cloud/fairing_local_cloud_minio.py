import uuid

from kubeflow import fairing

CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'fairing-python-cloud-job-{uuid.uuid4().hex[:4]}'

command = ["python", "tensorflow_mnist.py"]
output_map = {
    "Dockerfile": "Dockerfile",
    "tensorflow_mnist.py": "tensorflow_mnist.py"
}

fairing.config.set_preprocessor('python', command=command, path_prefix="/app", output_map=output_map)

# s3_endpoint = 'minio-service.kubeflow.svc.cluster.local:9000'
s3_endpoint = '192.168.21.38:31900'
minio_endpoint = "http://" + s3_endpoint
minio_username = "minio"
minio_key = "minio123"
minio_region = "us-east-1"

from kubeflow.fairing.builders.cluster.minio_context import MinioContextSource

context_source = MinioContextSource(endpoint_url=minio_endpoint, minio_secret=minio_username,
                                    minio_secret_key=minio_key, region_name=minio_region)

fairing.config.set_builder('cluster', registry=CONTAINER_REGISTRY, image_name="fairing-python-cloud-job",
                           dockerfile_path="Dockerfile",
                           namespace=namespace,
                           context_source=context_source)

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True)

fairing.config.run()
