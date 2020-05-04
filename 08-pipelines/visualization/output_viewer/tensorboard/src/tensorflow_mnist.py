from __future__ import absolute_import, division, print_function, unicode_literals

import json

import argparse
import tensorflow as tf


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tb_log_dir', default='./data/logs', type=str)
    args = parser.parse_args()

    tb_log_dir = args.tb_log_dir

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
    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)


if __name__ == '__main__':
    train()
