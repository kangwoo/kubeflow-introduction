from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os

import tensorflow as tf
import tensorflow_datasets as tfds


def build_and_compile_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])
    return model


@tfds.decode.make_decoder(output_dtype=tf.float32)
def decode_image(example, feature):
    return tf.cast(feature.decode_example(example), dtype=tf.float32) / 255


def train():
    print("TensorFlow version: ", tf.__version__)

    tf_config = os.environ.get('TF_CONFIG', '{}')
    print("TF_CONFIG %s", tf_config)
    tf_config_json = json.loads(tf_config)
    cluster = tf_config_json.get('cluster')
    job_name = tf_config_json.get('task', {}).get('type')
    task_index = tf_config_json.get('task', {}).get('index')
    print("cluster={} job_name={} task_index={}}", cluster, job_name, task_index)

    BATCH_SIZE = 64

    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
    mnist = tfds.builder('mnist', data_dir='./mnist')
    mnist.download_and_prepare()

    mnist_train, mnist_test = mnist.as_dataset(
        split=['train', 'test'],
        decoders={'image': decode_image()},
        as_supervised=True)
    train_input_dataset = mnist_train.cache().repeat().shuffle(
        buffer_size=50000).batch(BATCH_SIZE)
    eval_input_dataset = mnist_test.cache().repeat().batch(BATCH_SIZE)

    options = tf.data.Options()
    options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
    train_input_dataset = train_input_dataset.with_options(options)
    eval_input_dataset = eval_input_dataset.with_options(options)

    print("Training...")

    with strategy.scope():
        multi_worker_model = build_and_compile_model()

    num_train_examples = mnist.info.splits['train'].num_examples
    train_steps = num_train_examples // BATCH_SIZE
    train_epochs = 10

    multi_worker_model.fit(train_input_dataset, epochs=train_epochs, steps_per_epoch=train_steps)

    # Evaluate the model on test set
    score = multi_worker_model.evaluate(eval_input_dataset, steps=10)
    print('Test accuracy: ', score[1])


if __name__ == '__main__':
    train()
