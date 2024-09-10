output "vpc_id" {
  value = resource.tencentcloud_vpc.vpc.id
}

output "subnet_id" {
  value = resource.tencentcloud_subnet.subnet.id
}