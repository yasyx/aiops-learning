output "public_ip" {
  value = module.tencent_cvm.public_ip
}

output "kube_config" {
  value = "export KUBECONFIG=./config.yaml"
}