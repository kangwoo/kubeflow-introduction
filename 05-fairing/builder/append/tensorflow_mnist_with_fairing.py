from __future__ import absolute_import, division, print_function, unicode_literals

import os


def train():
    import tensorflow as tf

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
    print("Training...")
    model.fit(x_train, y_train, epochs=5, validation_split=0.2)

    # Evaluate the model on test set
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score[1])


def fairing_run():
    import uuid
    from kubeflow import fairing

    CONTAINER_REGISTRY = 'kangwoo'

    namespace = 'admin'
    job_name = f'fairing-python-append-job-runtime-{uuid.uuid4().hex[:4]}'

    fairing.config.set_preprocessor('python', executable="tensorflow_mnist_with_fairing.py")

    fairing.config.set_builder('append', registry=CONTAINER_REGISTRY,
                               image_name="fairing-python-append-job-runtime",
                               base_image="tensorflow/tensorflow:2.1.0-py3")

    fairing.config.set_deployer('job', namespace=namespace, job_name=job_name, cleanup=False, stream_log=True)

    fairing.config.run()


if __name__ == '__main__':
    if os.getenv('FAIRING_RUNTIME', None) is None:
        fairing_run()
    else:
        train()
