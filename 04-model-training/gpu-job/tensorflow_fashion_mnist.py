from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical


def build_and_compile_model():
    x_in = Input(shape=(28, 28, 1))
    x = Conv2D(filters=64, kernel_size=2, padding='same', activation='relu')(x_in)
    x = MaxPooling2D(pool_size=2)(x)
    x = Dropout(0.3)(x)

    x = Conv2D(filters=32, kernel_size=2, padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=2)(x)
    x = Dropout(0.3)(x)

    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x_out = Dense(10, activation='softmax')(x)

    cnn = Model(inputs=x_in, outputs=x_out)
    cnn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return cnn


def train():
    print("TensorFlow version: ", tf.__version__)

    gpus = tf.config.experimental.list_physical_devices('GPU')
    print("GPUs", gpus)
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
        tf.config.experimental.set_virtual_device_configuration(gpu, [
            tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    print('x_train shape:', x_train.shape, 'y_train shape:', y_train.shape)

    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255
    x_train = np.reshape(x_train, x_train.shape + (1,))
    x_test = np.reshape(x_test, x_test.shape + (1,))
    print('x_train shape:', x_train.shape, 'x_test shape:', x_test.shape)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    print('y_train shape:', y_train.shape, 'y_test shape:', y_test.shape)

    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = build_and_compile_model()

    model.summary()
    model.fit(x_train, y_train, batch_size=64, epochs=10, validation_split=0.2)

    # Evaluate the model on test set
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test accuracy: ', score[1])


if __name__ == '__main__':
    train()
