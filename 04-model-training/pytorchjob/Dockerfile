FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime

RUN pip install tensorboardX==1.9.0

WORKDIR /app
COPY mnist.py /app

ENTRYPOINT ["python", "/app/mnist.py"]