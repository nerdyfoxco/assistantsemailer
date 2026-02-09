variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "project_name" {
  default = "assistants-co"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}
