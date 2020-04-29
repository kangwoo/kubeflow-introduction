#!/bin/bash -e

image_name=kangwoo/tensorflow-2.1.0-notebook-cpu
image_tag=1.0.0
full_image_name=${image_name}:${image_tag}
base_image=tensorflow/tensorflow:2.1.0-py3-jupyter

cd "$(dirname "$0")"

docker build --build-arg BASE_IMAGE=$base_image -t "$full_image_name" .
docker push "$full_image_name"

