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


@tool
def modify_config(service_name: str, key: str , value: str) -> str:
    """Implementation to modify Kubernetes config""" 
    
    print("2. The Function [modify_config] was called!!!\n")
    
    return f"The config of {service_name} was modified, detail: modify the value of {key} to {value}"
   
@tool
def restart_service(service_name):
    """Implementation to restart a Kubernetes service"""
    
    print("2. The Function [restart_service] was called!!!\n")  # Debugging purpose
    
    return f"The service of {service_name} was restarted"

@tool
def apply_manifest(resouce_type: str, image: str):
    """Implementation to apply Kubernetes manifest"""

    print("2. The Function [apply_manifest] was called!!! \n")  # Debugging purpose
    
    return f"A new {resouce_type} manifest was applied with image: {image}"
    

all_tools_map = {
    "get_k8s_version": get_k8s_version,
    "get_k8s_pods": get_k8s_pods,
    "modify_config": modify_config,
    "restart_service": restart_service,
    "apply_manifest": apply_manifest,
    # Add more tools here...
}

all_tools = [
    get_k8s_pods,
    get_k8s_version,
    modify_config,
    restart_service,
    apply_manifest,
    # Add more tools here...
]