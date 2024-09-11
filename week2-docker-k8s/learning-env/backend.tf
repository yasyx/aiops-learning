terraform {
  backend "oss" {
    bucket = "yasy-tf-state"
    prefix = "week2-docker-k8s"
  }
}