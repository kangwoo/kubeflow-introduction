from typing import NamedTuple

import kfp
from kubernetes.client.models import V1EnvVar


def train(tb_log_dir: str) -> NamedTuple('Outputs', [('mlpipeline_ui_metadata', 'ui_metadata'),
                                                     ('mlpipeline_metrics', 'metrics')]):
    import tensorflow as tf
    import json

    print("TensorFlow version: ", tf.__version__)

    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    callbacks = [tf.keras.callbacks.TensorBoard(log_dir=tb_log_dir)]

    print("Training...")
    model.fit(x_train, y_train, epochs=5, validation_split=0.2, callbacks=callbacks)

    score = model.evaluate(x_test, y_test, batch_size=128)
    print('Test accuracy: ', score[1])

    metadata = {
        'outputs': [{
            'type': 'tensorboard',
            'source': tb_log_dir,
        }]
    }

    loss = score[0]
    accuracy = score[1]
    metrics = {
        'metrics': [{
            'name': 'accuracy',
            'numberValue': float(accuracy),
            'format': "PERCENTAGE",
        }, {
            'name': 'loss',
            'numberValue': float(loss),
            'format': "RAW",
        }]
    }

    from collections import namedtuple
    outputs = namedtuple('Outputs', ['mlpipeline_ui_metadata', 'mlpipeline_metrics'])
    return outputs(json.dumps(metadata), json.dumps(metrics))


train_op = kfp.components.func_to_container_op(train, base_image='tensorflow/tensorflow:2.1.0-py3')


def lightweight_tensorboard_pipeline(tb_log_dir):
    s3_endpoint = 'minio-service.kubeflow.svc.cluster.local:9000'
    minio_endpoint = "http://" + s3_endpoint
    minio_username = "minio"
    minio_key = "minio123"
    minio_region = "us-east-1"

    train_op(tb_log_dir).add_env_variable(V1EnvVar(name='S3_ENDPOINT', value=s3_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ENDPOINT_URL', value=minio_endpoint)) \
        .add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value=minio_username)) \
        .add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value=minio_key)) \
        .add_env_variable(V1EnvVar(name='AWS_REGION', value=minio_region)) \
        .add_env_variable(V1EnvVar(name='S3_USE_HTTPS', value='0')) \
        .add_env_variable(V1EnvVar(name='S3_VERIFY_SSL', value='0'))


if __name__ == '__main__':
    arguments = {'tb_log_dir': 's3://tensorboard/lightweight'}
    my_run = kfp.Client().create_run_from_pipeline_func(lightweight_tensorboard_pipeline,
                                                        arguments=arguments,
                                                        experiment_name='Visualization Experiment')
