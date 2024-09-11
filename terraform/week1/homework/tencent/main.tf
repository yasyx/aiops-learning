# 创建vpc 和 subnet
module "network" {
  source            = "../../../modules/tecent/network"
  availability_zone = var.availability_zone
}

// 创建腾讯云虚拟机 内存8G
module "docker_cvm" {
  depends_on = [ module.network ]
  source            = "../../../modules/tecent/cvm"
  memory_size       = var.memory_size
  cpu_core_count    = var.cpu_core_count
  availability_zone = var.availability_zone
  instance_name     = "docker-cvm"
  subnet_id         = module.network.subnet_id
  vpc_id            = module.network.vpc_id
}

module "k3s_cvm" {
  depends_on = [ module.network ]
  source            = "../../../modules/tecent/cvm"
  memory_size       = var.memory_size
  cpu_core_count    = var.cpu_core_count
  availability_zone = var.availability_zone
  instance_name     = "k3s-cvm"
  subnet_id         = module.network.subnet_id
  vpc_id            = module.network.vpc_id
}

# k3s 安装
module "k3s" {
  depends_on = [ module.k3s_cvm ]
  source     = "../../../modules/k3s"
  user       = var.user
  password   = var.password
  public_ip  = module.k3s_cvm.public_ip
  private_ip = module.k3s_cvm.private_ip
}

provider "helm" {
  kubernetes {
    config_path = local_sensitive_file.kubeconfig.filename
  }
}

# argocd 安装
module "argocd" {
  depends_on = [ module.k3s ]
  source      = "../../../modules/helm"
  name        = "argocd"
  namespace   = "argocd"
  chart       = "argo-cd"
  repository  = "https://argoproj.github.io/argo-helm"
}

# crossplan 安装
module "crossplane" {
  depends_on = [ module.k3s ]
  source      = "../../../modules/helm"
  name        = "crossplane"
  repository  = "https://charts.crossplane.io/stable"
  chart       = "crossplane"
  namespace   = "crossplane-system"

}

// 获取 kubeconfig
resource "local_sensitive_file" "kubeconfig" {
  content  = module.k3s.kube_config
  filename = "${path.module}/config.yaml"
}

// 安装 Docker
resource "terraform_data" "install_docker" {
  depends_on = [ module.docker_cvm ]
  provisioner "file" {
    connection {
      password = var.password
      host     = module.docker_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    source      = "./scripts/docker-install.sh"
    destination = "/tmp/docker-install.sh"
  }
  provisioner "remote-exec" {
    connection {
      password = var.password
      host     = module.docker_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    inline = [
      "chmod +x /tmp/docker-install.sh",
      "bash /tmp/docker-install.sh"
    ]
  }
}