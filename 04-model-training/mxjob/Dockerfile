FROM mxnet/python:1.5.0_cpu_py3

WORKDIR /app
COPY image_classification.py /app
COPY data.py /app

CMD ["python3", "image_classification.py", "--dataset", "cifar10", "--model", "vgg11", "--epochs", "1", "--kvstore", "dist_sync"]