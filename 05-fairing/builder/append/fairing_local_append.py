import uuid

from kubeflow import fairing

CONTAINER_REGISTRY = 'kangwoo'

namespace = 'admin'
job_name = f'fairing-python-append-job-{uuid.uuid4().hex[:4]}'

fairing.config.set_preprocessor('python', executable="tensorflow_mnist.py")

fairing.config.set_builder('append', registry=CONTAINER_REGISTRY, image_name="fairing-python-append-job",
                           base_image="tensorflow/tensorflow:2.1.0-py3")

fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True)

fairing.config.run()
