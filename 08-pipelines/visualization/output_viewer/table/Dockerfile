FROM python:3.6.10-slim

RUN pip install sklearn pandas

WORKDIR /app
COPY ./src /app

CMD ["python", "/app/table_inline.py"]