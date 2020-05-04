import kfp
import kfp.dsl as dsl


@dsl.pipeline(
    name="Sidecard pipeline",
    description="Sidecard pipeline"
)
def sidecar_pipeline(sleep_sec: int = 30):
    # sidecar with sevice that reply "hello world" to any GET request
    echo = dsl.Sidecar(
        name="echo",
        image="hashicorp/http-echo:latest",
        args=['-text="hello world"'],
    )

    # container op with sidecar
    op1 = dsl.ContainerOp(
        name="download",
        image="busybox:latest",
        command=["sh", "-c"],
        arguments=[
            "sleep %s; wget localhost:5678 -O /tmp/results.txt" % sleep_sec
        ],  # sleep for X sec and call the sidecar and save results to output
        sidecars=[echo],
        file_outputs={"downloaded": "/tmp/results.txt"},
    )

    op2 = dsl.ContainerOp(
        name="echo",
        image="library/bash",
        command=["sh", "-c"],
        arguments=["echo %s" % op1.output],  # print out content of op1 output
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(sidecar_pipeline, __file__ + '.zip')

    client = kfp.Client()
    my_experiment = client.create_experiment(name='Sample Experiment')
    my_run = client.run_pipeline(my_experiment.id, 'Sidecard pipeline', __file__ + '.zip')
