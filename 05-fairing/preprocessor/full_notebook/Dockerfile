FROM tensorflow/tensorflow:2.1.0-py3

RUN pip install papermill \
    && pip install s3 gcloud azure==4.0.0 \
    && pip install ipykernel \
    && python -m ipykernel install