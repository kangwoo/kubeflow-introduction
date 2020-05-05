import argparse
import base64
import io
import logging
from typing import Dict

import kfserving
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

logging.basicConfig(level=kfserving.constants.KFSERVING_LOGLEVEL)

transform = transforms.Compose([
    transforms.Resize(32),
    transforms.CenterCrop(32),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


def image_transform(instance):
    byte_array = base64.b64decode(instance['image']['b64'])
    image = Image.open(io.BytesIO(byte_array))
    im = Image.fromarray(np.asarray(image))
    res = transform(im)
    logging.info(res)
    return res.tolist()


CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


def top_5(prediction):
    pred = torch.as_tensor(prediction)
    scores = torch.nn.functional.softmax(pred, dim=0)

    _, top_5 = torch.topk(pred, 5)

    results = {}
    for idx in top_5:
        results[CLASSES[idx]] = scores[idx].item()

    return results


class ImageTransformer(kfserving.KFModel):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host

    def preprocess(self, inputs: Dict) -> Dict:
        return {'instances': [image_transform(instance) for instance in inputs['instances']]}

    def postprocess(self, inputs: Dict) -> Dict:
        return {'predictions': [top_5(prediction) for prediction in inputs['predictions']]}


if __name__ == "__main__":
    DEFAULT_MODEL_NAME = "model"

    parser = argparse.ArgumentParser(parents=[kfserving.kfserver.parser])
    parser.add_argument('--model_name', default=DEFAULT_MODEL_NAME,
                        help='The name that the model is served under.')
    parser.add_argument('--predictor_host', help='The URL for the model predict function', required=True)

    args, _ = parser.parse_known_args()

    transformer = ImageTransformer(args.model_name, predictor_host=args.predictor_host)
    kfserver = kfserving.KFServer()
    kfserver.start(models=[transformer])