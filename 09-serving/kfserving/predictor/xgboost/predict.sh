CLUSTER_IP=192.168.21.38:32380
MODEL_NAME=sklearn-iris
SERVICE_HOSTNAME=$(kubectl -n admin get inferenceservice sklearn-iris -o jsonpath='{.status.url}' | cut -d "/" -f 3)

INPUT_PATH=@./iris-input.json
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${CLUSTER_IP}/v1/models/${MODEL_NAME}:predict -d ${INPUT_PATH}