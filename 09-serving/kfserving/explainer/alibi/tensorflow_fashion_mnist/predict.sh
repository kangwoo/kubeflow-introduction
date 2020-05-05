CLUSTER_IP=192.168.21.38:32380
MODEL_NAME=custom-hello
SERVICE_HOSTNAME=$(kubectl -n admin get inferenceservice custom-hello -o jsonpath='{.status.url}' | cut -d "/" -f 3)

curl -v -H "Host: ${SERVICE_HOSTNAME}" http://${CLUSTER_IP}/v1/models/${MODEL_NAME}:predict