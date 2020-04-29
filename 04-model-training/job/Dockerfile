FROM python:3.6-slim

RUN pip install scikit-learn

WORKDIR /app
COPY sklearn_iris.py /app

ENTRYPOINT ["python", "/app/sklearn_iris.py"]
