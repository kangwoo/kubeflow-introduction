from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime, timezone

import argparse
import tensorflow as tf


def train():
    print("TensorFlow version: ", tf.__version__)

    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', default=0.01, type=float)
    parser.add_argument('--dropout', default=0.2, type=float)
    parser.add_argument('--epochs', default=10, type=int)
    args = parser.parse_args()

    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Reserve 10,000 samples for validation
    x_val = x_train[-10000:]
    y_val = y_train[-10000:]
    x_train = x_train[:-10000]
    y_train = y_train[:-10000]

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(args.dropout),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=args.learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    print("Training...")

    model.fit(x_train, y_train, batch_size=64, epochs=args.epochs,
              validation_data=(x_val, y_val))

    # Evaluate the model on the test data using `evaluate`
    print('\n# Evaluate on test data')
    results = model.evaluate(x_test, y_test, batch_size=128)
    print('test_loss:', results[0])
    print('test_accuracy:', results[1])



if __name__ == '__main__':
    train()
