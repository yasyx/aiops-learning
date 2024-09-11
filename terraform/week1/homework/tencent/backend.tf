terraform {
  backend "oss" {
    bucket = "yasy-tf-state"
    prefix = "tencentcloud"
  }
}