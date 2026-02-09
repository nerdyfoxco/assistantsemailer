variable "project_name" {
  default = "assistants-co"
}

variable "subnet_ids" {
  type = list(string)
}

variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}
