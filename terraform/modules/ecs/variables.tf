variable "project_name" {
  description = "Nome do projeto"
  type        = string
}

variable "environment" {
  description = "Ambiente"
  type        = string
}

variable "aws_region" {
  description = "Região AWS"
  type        = string
}

variable "cluster_name" {
  description = "Nome do cluster ECS"
  type        = string
}

variable "subnet_ids" {
  description = "Lista de subnets privadas"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Lista de security groups"
  type        = list(string)
}

variable "api_container_image" {
  description = "Imagem da API"
  type        = string
}

variable "frontend_container_image" {
  description = "Imagem do frontend"
  type        = string
}

variable "api_container_port" {
  description = "Porta da API"
  type        = number
  default     = 8000
}

variable "frontend_container_port" {
  description = "Porta do frontend"
  type        = number
  default     = 80
}

variable "api_cpu" {
  description = "CPU da task da API"
  type        = number
  default     = 256
}

variable "api_memory" {
  description = "Memória da task da API"
  type        = number
  default     = 512
}

variable "frontend_cpu" {
  description = "CPU da task do frontend"
  type        = number
  default     = 256
}

variable "frontend_memory" {
  description = "Memória da task do frontend"
  type        = number
  default     = 512
}

variable "desired_count_api" {
  description = "Quantidade desejada da API"
  type        = number
  default     = 1
}

variable "desired_count_frontend" {
  description = "Quantidade desejada do frontend"
  type        = number
  default     = 1
}

variable "tags" {
  description = "Tags padrão"
  type        = map(string)
  default     = {}
}

variable "api_target_group_arn" {
  description = "ARN do target group da API"
  type        = string
}

variable "frontend_target_group_arn" {
  description = "ARN do target group do frontend"
  type        = string
}