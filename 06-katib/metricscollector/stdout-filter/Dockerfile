FROM tensorflow/tensorflow:2.1.0-py3

WORKDIR /app
ADD katib_stdout_filter.py /app

ENTRYPOINT ["python", "/app/katib_stdout_filter.py"]