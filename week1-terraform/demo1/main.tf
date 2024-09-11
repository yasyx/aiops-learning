module "network" {
  source = "../modules/tecent/network"
  availability_zone = "ap-hongkong"
}
module "tencentcloud-cvm" {
  source = "../modules/tecent/cvm"
  vpc_id = module.network.vpc_id
  subnet_id = module.network.subnet_id
  instance_name = "tecent"
  memory_size = 8
}