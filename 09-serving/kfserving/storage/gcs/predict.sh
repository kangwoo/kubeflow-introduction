CLUSTER_IP=192.168.21.38:32380
MODEL_NAME=mnist-s3
SERVICE_HOSTNAME=$(kubectl -n admin get inferenceservice mnist-s3 -o jsonpath='{.status.url}' | cut -d "/" -f 3)

INPUT_PATH=@./mnist-input.json
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${CLUSTER_IP}/v1/models/${MODEL_NAME}:predict -d ${INPUT_PATH}