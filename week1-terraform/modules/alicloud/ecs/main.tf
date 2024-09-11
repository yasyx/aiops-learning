
data "alicloud_instance_types" "instance_types" {
  cpu_core_count = var.cpu_core_count
  memory_size = var.memory_size
}