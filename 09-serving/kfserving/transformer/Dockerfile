FROM python:3.6-slim

RUN pip install torch torchvision
RUn pip install kfserving==0.3.0 image numpy

WORKDIR /app
ADD image_transformer.py /app/

ENTRYPOINT ["python", "image_transformer.py"]