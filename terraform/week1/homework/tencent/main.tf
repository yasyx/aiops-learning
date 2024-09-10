// 创建腾讯云虚拟机 内存8G
module "tencentcloud_cvm" {
  source      = "../../../modules/tecent/cvm"
  memory_size = var.memory_size
  cpu_core_count = var.cpu_core_count
  availability_zone = var.availability_zone
}

# # k3s 安装
# module "k3s" {
#   source = "../../../modules/k3s"
#   user = var.user
#   password = var.password
#   public_ip = module.tencentcloud_cvm.public_ip
#   private_ip = module.tencentcloud_cvm.private_ip
# }

# # argocd 安装
# module "argocd" {
#   source = "../modules/helm"
#   kube_config = local_sensitive_file.kubeconfig.filename
#   name = "argocd"
#   namespace = "argocd"
#   chart = "argo-cd"
#   repository = "https://argoproj.github.io/argo-helm"
# }

# // 获取 kubeconfig
# resource "local_sensitive_file" "kubeconfig" {
#   content  = module.k3s.kube_config
#   filename = "${path.module}/config.yaml"
# }

// 安装 Docker
resource "terraform_data" "install_docker" {
  provisioner "file" {
    connection {
      password = var.password
      host     = module.tencentcloud_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    source      = "./scripts/docker-install.sh"
    destination = "/tmp/docker-install.sh"
  }
  provisioner "remote-exec" {
    connection {
      password = var.password
      host     = module.tencentcloud_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    inline = [
      "chmod +x /tmp/docker-install.sh",
      "bash /tmp/docker-install.sh"
    ]
  }
}