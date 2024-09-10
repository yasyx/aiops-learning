module "alicloud-ecs" {
  source = "../../../modules/alicloud/ecs"
  cpu_core_count = 2
  memory_size = 2
}