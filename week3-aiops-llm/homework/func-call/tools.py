from langchain_core.tools import tool

@tool
def get_k8s_version():
    """Fetches the Kubernetes version."""
    # Implementation to fetch Kubernetes version
    return "v1.23.10"
@tool
def get_k8s_pods():
    """Fetches all Kubernetes pods."""
    # Implementation to fetch Kubernetes pods
    return [{"name": "pod1", "status": "running"}, {"name": "pod2", "status": "pending"}]



all_tools_map = {
    "get_k8s_version": get_k8s_version,
    "get_k8s_pods": get_k8s_pods,
    # Add more tools here...
}

all_tools = [
    get_k8s_pods,
    get_k8s_version
]