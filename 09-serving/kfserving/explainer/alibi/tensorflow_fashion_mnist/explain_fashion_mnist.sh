import json
import os
import ssl

import argparse
import matplotlib.pyplot as plt
import numpy as np
import requests
import tensorflow as tf

ssl._create_default_https_context = ssl._create_unverified_context

HOST = 'alibi-fashion-mnist.admin.example.com'
PREDICT_TEMPLATE = 'http://{0}/v1/models/alibi-fashion-mnist:predict'
EXPLAIN_TEMPLATE = 'http://{0}/v1/models/alibi-fashion-mnist:explain'


def get_image_data(idx):
    (_, _), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

    return x_test[idx]


def preprocess_input(input):
    data = input.astype('float32') / 255
    data = np.reshape(data, data.shape + (1,))
    data = data.reshape(1, 28, 28, 1)
    return data


CLASSES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


def decode_predictions(predictions):
    labels = np.argmax(predictions, axis=1)
    return CLASSES[labels[0]]


def predict(cluster_ip):
    image_data = get_image_data(0)
    data = preprocess_input(image_data)
    payload = json.dumps({"instances": data.tolist()})

    headers = {'Host': HOST}
    url = PREDICT_TEMPLATE.format(cluster_ip)
    print("Calling ", url)
    r = requests.post(url, data=payload, headers=headers)
    resp_json = json.loads(r.content.decode('utf-8'))
    preds = np.array(resp_json["predictions"])
    label = decode_predictions(preds)

    plt.imshow(image_data)
    plt.title(label)
    plt.show()


def explain(cluster_ip):
    image_data = get_image_data(1)
    data = preprocess_input(image_data)
    payload = json.dumps({"instances": data.tolist()})

    headers = {'Host': HOST}
    url = EXPLAIN_TEMPLATE.format(cluster_ip)
    print("Calling ", url)
    r = requests.post(url, data=payload, headers=headers)
    if r.status_code == 200:
        explanation = json.loads(r.content.decode('utf-8'))

        exp_arr = np.array(explanation['anchor'])

        f, axarr = plt.subplots(1, 2)
        axarr[0].imshow(image_data)
        axarr[1].imshow(exp_arr[:, :, 0])
        plt.show()
    else:
        print("Received response code and content", r.status_code, r.content)


parser = argparse.ArgumentParser()
parser.add_argument('--cluster_ip', default=os.environ.get("CLUSTER_IP"), help='Address of istio-ingress-gateway')
parser.add_argument('--op', choices=["predict", "explain"], default="predict",
                    help='Operation to run')
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    if args.op == "predict":
        predict(args.cluster_ip)
    elif args.op == "explain":
        explain(args.cluster_ip)
