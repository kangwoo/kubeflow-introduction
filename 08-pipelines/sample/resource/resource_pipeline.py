import kfp
from kfp import dsl
import json

_job_manifest = """
{
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "generateName": "kfp"
    },
    "spec": {
        "template": {
            "metadata": {
                "name": "resource-pipeline"
            },
            "spec": {
                "containers": [{
                    "name": "mnist",
                    "image": "kangwoo/pipelines-tensorflow-mnist:0.0.1",
                    "command": ["python", "/app/tensorflow_mnist.py"]
                }],
                "restartPolicy": "Never"
            }
        }   
    }
}
"""


@dsl.pipeline(
    name='Kubernetes Resource',
    description='Kubernetes Resource'
)
def resource_pipeline():
    op = dsl.ResourceOp(
        name='resource-job',
        k8s_resource=json.loads(_job_manifest),
        action='create'
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(resource_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Resource pipeline', __file__ + '.zip')
