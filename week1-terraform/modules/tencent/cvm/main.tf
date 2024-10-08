
# Get availability zones
data "tencentcloud_availability_zones_by_product" "default" {
  product = "cvm"
  include_unavailable = false
  name = var.availability_zone
}

# Get availability images
data "tencentcloud_images" "default" {
  image_type = ["PUBLIC_IMAGE"]
  os_name    = "ubuntu"
}

# Get availability instance types
data "tencentcloud_instance_types" "default" {
  cpu_core_count = var.cpu_core_count
  memory_size    = var.memory_size
}

# Create a web server
resource "tencentcloud_instance" "web" {
  instance_name              = var.instance_name
  availability_zone          = data.tencentcloud_availability_zones_by_product.default.zones.0.name
  image_id                   = data.tencentcloud_images.default.images.0.image_id
  instance_type              = data.tencentcloud_instance_types.default.instance_types.0.instance_type
  spot_instance_type         = "ONE-TIME"
  spot_max_price             = 1
  instance_charge_type       = "SPOTPAID"
  system_disk_type           = "CLOUD_BSSD"
  system_disk_size           = 50
  allocate_public_ip         = true
  internet_max_bandwidth_out = 20
  orderly_security_groups    = [tencentcloud_security_group.default.id]
  password                   = "password123"
  vpc_id                     = var.vpc_id
  subnet_id                  = var.subnet_id
}

# Create security group
resource "tencentcloud_security_group" "default" {
  name        = "web accessibility"
  description = "make it accessible for both production and stage ports"
}

# Create security group rule allow ssh request
resource "tencentcloud_security_group_rule_set" "ssh" {
  security_group_id = tencentcloud_security_group.default.id
  ingress {
    action      = "ACCEPT"
    cidr_block  = "0.0.0.0/0"
    protocol    = "TCP"
    port        = "22,80,443,6443"
    description = "A:Allow Ips and 80"
  }

  egress {
    action = "ACCEPT"
    cidr_block = "0.0.0.0/0"
    protocol    = "ALL"
    port        = "ALL"
    description = " ALLOW ALL"
  }
  
}