# The settings below must match their equivalents, if applicable, in:
# * resemble/settings.h
# * <possibly other languages by the time you read this>

# gRPC max message size to transmit large actor state data.
MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES = 100 * 1024 * 1024

ENVOY_PROXY_IMAGE = 'envoyproxy/envoy:v1.24.0'

# The path to the directory where Resemble state is stored.
RESEMBLE_STATE_DIRECTORY = '/var/run/resemble/state'

# The names of environment variables that are only present when running in `rsm dev`.
ENVVAR_RSM_DEV = 'RSM_DEV'
ENVVAR_RSM_DEV_NAME = 'RSM_DEV_NAME'
ENVVAR_RSM_DOT_RSM_DEV_DIRECTORY = 'RSM_DOT_RSM_DEV_DIRECTORY'
ENVVAR_RSM_DEV_LOCAL_ENVOY = 'RSM_DEV_LOCAL_ENVOY'
ENVVAR_RSM_DEV_LOCAL_ENVOY_PORT = 'RSM_DEV_LOCAL_ENVOY_PORT'
ENVVAR_RSM_DEV_INSPECT_PORT = 'RSM_DEV_INSPECT_PORT'

# The name of an environment variable that's only present when running on
# Kubernetes.
ENVVAR_KUBERNETES_SERVICE_HOST = 'KUBERNETES_SERVICE_HOST'
