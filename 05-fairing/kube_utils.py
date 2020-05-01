from kubernetes.client.models.v1_resource_requirements import V1ResourceRequirements


def get_gpu_resource_mutator(gpu=None, gpu_vendor='nvidia'):
    def _resource_mutator(kube_manager, pod_spec, namespace):  # pylint:disable=unused-argument
        if gpu is None:
            return
        if pod_spec.containers and len(pod_spec.containers) >= 1:
            limits = {}
            if gpu:
                limits['{}.com/gpu'.format(gpu_vendor)] = gpu
            if pod_spec.containers[0].resources:
                if pod_spec.containers[0].resources.limits:
                    pod_spec.containers[0].resources.limits = {}
                for k, v in limits.items():
                    pod_spec.containers[0].resources.limits[k] = v
            else:
                pod_spec.containers[0].resources = V1ResourceRequirements(limits=limits)

    return _resource_mutator


def get_annotation_mutator(annotations=None):
    def _annotation_mutator(kube_manager, pod_spec, namespace):  # pylint:disable=unused-argument
        if annotations is None:
            return
        if pod_spec.containers and len(pod_spec.containers) >= 1:
            limits = {}
            if annotations:
                pod_spec
                limits['{}.com/gpu'.format(gpu_vendor)] = gpu
            if pod_spec.containers[0].resources:
                if pod_spec.containers[0].resources.limits:
                    pod_spec.containers[0].resources.limits = {}
                for k, v in limits.items():
                    pod_spec.containers[0].resources.limits[k] = v
            else:
                pod_spec.containers[0].resources = V1ResourceRequirements(limits=limits)

    return _resource_mutator