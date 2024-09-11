# 创建vpc 和 subnet
module "network" {
  source            = "../../week1-terraform/modules/tencent/network"
  availability_zone = var.availability_zone
}

// 创建腾讯云虚拟机 内存8G
module "tencent_cvm" {
  depends_on = [ module.network ]
  source            = "../../week1-terraform/modules/tencent/cvm"
  memory_size       = var.memory_size
  cpu_core_count    = var.cpu_core_count
  availability_zone = var.availability_zone
  instance_name     = "tencent-cvm"
  subnet_id         = module.network.subnet_id
  vpc_id            = module.network.vpc_id
}


# k3s 安装
module "k3s" {
  depends_on = [ module.tencent_cvm ]
  source     = "../../week1-terraform/modules/k3s"
  user       = var.user
  password   = var.password
  public_ip  = module.tencent_cvm.public_ip
  private_ip = module.tencent_cvm.private_ip
}


// 获取 kubeconfig
resource "local_sensitive_file" "kubeconfig" {
  content  = module.k3s.kube_config
  filename = "${path.module}/config.yaml"
}

// 安装 Docker
resource "terraform_data" "install_docker" {
  depends_on = [ module.tencent_cvm ]
  provisioner "file" {
    connection {
      password = var.password
      host     = module.tencent_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    source      = "./scripts/docker-install.sh"
    destination = "/tmp/docker-install.sh"
  }
  provisioner "remote-exec" {
    connection {
      password = var.password
      host     = module.tencent_cvm.public_ip
      type     = "ssh"
      user     = var.user
    }
    inline = [
      "chmod +x /tmp/docker-install.sh",
      "bash /tmp/docker-install.sh"
    ]
  }
}


