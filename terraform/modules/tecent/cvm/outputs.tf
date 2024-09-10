output "public_ip" {
  value = resource.tencentcloud_instance.web.public_ip
}

output "private_ip" {
  value = resource.tencentcloud_instance.web.private_ip
}