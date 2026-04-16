variable "project_name" {
  description = "Nome base do projeto"
  type        = string
}

variable "environment" {
  description = "Ambiente"
  type        = string
}

variable "repositories" {
  description = "Lista de repositórios ECR"
  type        = list(string)
}

variable "tags" {
  description = "Tags padrão"
  type        = map(string)
  default     = {}
}