variable "project_name" {
  description = "Nome do projeto"
  type        = string
}

variable "environment" {
  description = "Ambiente"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR da VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "Lista de CIDRs das subnets públicas"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "Lista de CIDRs das subnets privadas"
  type        = list(string)
}

variable "availability_zones" {
  description = "Lista de AZs"
  type        = list(string)
}

variable "tags" {
  description = "Tags padrão"
  type        = map(string)
  default     = {}
}