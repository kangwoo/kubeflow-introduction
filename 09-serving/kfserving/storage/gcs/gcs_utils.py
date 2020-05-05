import os

from kubernetes import client

GCSCredentialFileName = "gcloud-application-credentials.json"
GCSCredentialVolumeName = "user-gcp-sa"
GCSCredentialVolumeMountPath = "/var/secrets/"
GCSCredentialEnvKey = "GOOGLE_APPLICATION_CREDENTIALS"


def gcp_credentials(secret_name='user-gcp-sa', credential_file_name=GCSCredentialFileName):
    def _add_gcp_credentials(kube_manager, pod_spec, namespace):
        """add GCP credential

        :param kube_manager: kube manager for handles communication with Kubernetes' client
        :param pod_spec: pod spec like volumes and security context
        :param namespace: The custom resource

        """
        if not kube_manager.secret_exists(secret_name, namespace):
            raise ValueError('Unable to mount credentials: Secret {}} not found in namespace {}'
                             .format(secret_name, namespace))

        # volume_mount
        volume_mount = client.V1VolumeMount(
            name=GCSCredentialVolumeName, mount_path=GCSCredentialVolumeMountPath)
        if pod_spec.containers[0].volume_mounts:
            pod_spec.containers[0].volume_mounts.append(volume_mount)
        else:
            pod_spec.containers[0].volume_mounts = [volume_mount]

        volume = client.V1Volume(
            name=GCSCredentialVolumeName,
            secret=client.V1SecretVolumeSource(secret_name=secret_name))
        if pod_spec.volumes:
            pod_spec.volumes.append(volume)
        else:
            pod_spec.volumes = [volume]

        # environment
        credential_file_path = os.path.join(GCSCredentialVolumeMountPath, GCSCredentialFileName)
        env = [
            client.V1EnvVar(name=GCSCredentialEnvKey, value=credential_file_path),
        ]

        if pod_spec.containers[0].env:
            pod_spec.containers[0].env.extend(env)
        else:
            pod_spec.containers[0].env = env

    return _add_gcp_credentials
