CLUSTER_IP=192.168.21.38:32380
MODEL_NAME=pytorch-cifar10
SERVICE_HOSTNAME=$(kubectl -n admin get inferenceservice pytorch-cifar10 -o jsonpath='{.status.url}' | cut -d "/" -f 3)

INPUT_PATH=@./cifar10-input.json
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://$CLUSTER_IP/v1/models/$MODEL_NAME:predict -d $INPUT_PATH