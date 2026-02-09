variable "project_name" {
  default = "assistants-co"
}

variable "eks_cluster_role_arn" {
  type = string
}

variable "eks_node_role_arn" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}
