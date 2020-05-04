import kfp
from kfp import dsl


@dsl.pipeline(
    name='Volume pipeline',
    description='Volume pipeline'
)
def volume_pipeline():
    vop = dsl.VolumeOp(
        name="pipeline-volume",
        resource_name="pipeline-pvc",
        modes=dsl.VOLUME_MODE_RWO,
        size="100Mi"
    )

    step1 = dsl.ContainerOp(
        name='Flip coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import random; result = \'heads\' if random.randint(0,1) == 0 '
                   'else \'tails\'; print(result)" | tee /data/output'],
        pvolumes={"/data": vop.volume}
    )

    step2 = dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['cat', '/data/output'],
        pvolumes={"/data": step1.pvolume}
    )

    vop.delete().after(step2)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(volume_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Volume pipeline', __file__ + '.zip')
