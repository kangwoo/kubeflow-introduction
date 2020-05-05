from kubeflow.fairing.constants import constants
from kubernetes import client


def aws_credentials(secret_name=constants.AWS_CREDS_SECRET_NAME):
    def _add_aws_credentials(kube_manager, pod_spec, namespace):
        """add AWS credential

        :param kube_manager: kube manager for handles communication with Kubernetes' client
        :param pod_spec: pod spec like volumes and security context
        :param namespace: The custom resource

        """
        if not kube_manager.secret_exists(secret_name, namespace):
            raise ValueError('Unable to mount credentials: Secret {}} not found in namespace {}'
                             .format(secret_name, namespace))

        secret = client.CoreV1Api().read_namespaced_secret(secret_name, namespace)
        annotations = secret.metadata.annotations
        s3_endpoint = annotations['serving.kubeflow.org/s3-endpoint']
        s3_use_https = annotations['serving.kubeflow.org/s3-usehttps']
        s3_verify_ssl = annotations['serving.kubeflow.org/s3-verifyssl']

        env = [
            client.V1EnvVar(
                name='AWS_ACCESS_KEY_ID',
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name,
                        key='awsAccessKeyID'
                    )
                )
            ),
            client.V1EnvVar(
                name='AWS_SECRET_ACCESS_KEY',
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name,
                        key='awsSecretAccessKey'
                    )
                )
            ),
            client.V1EnvVar(name='S3_ENDPOINT', value=s3_endpoint),
            client.V1EnvVar(name='S3_USE_HTTPS', value=s3_use_https),
            client.V1EnvVar(name='S3_VERIFY_SSL', value=s3_verify_ssl),

        ]

        if pod_spec.containers[0].env:
            pod_spec.containers[0].env.extend(env)
        else:
            pod_spec.containers[0].env = env

    return _add_aws_credentials
