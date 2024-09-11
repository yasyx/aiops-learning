output "docker_cvm_public_ip" {
  value = module.docker_cvm.public_ip
}


output "k3s_cvm_public_ip" {
  value = module.k3s_cvm.public_ip
}