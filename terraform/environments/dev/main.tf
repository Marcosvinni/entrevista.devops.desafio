terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
  repositories = var.repositories
  tags         = var.tags
}

module "vpc" {
  source = "../../modules/vpc"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones   = var.availability_zones
  tags                 = var.tags
}

resource "aws_security_group" "ecs_services" {
  name        = "${var.project_name}-${var.environment}-ecs-sg"
  description = "Security group for ECS services"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-ecs-sg"
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  )
}

resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-${var.environment}-alb-sg"
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  )
}

module "alb" {
  source = "../../modules/alb"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  security_group_ids = [aws_security_group.alb.id]
  tags               = var.tags
}

module "ecs" {
  source = "../../modules/ecs"

  project_name              = var.project_name
  environment               = var.environment
  aws_region                = var.aws_region
  cluster_name              = "${var.project_name}-${var.environment}-cluster"
  subnet_ids                = module.vpc.private_subnet_ids
  security_group_ids        = [aws_security_group.ecs_services.id]
  api_container_image       = "nginx:alpine"
  frontend_container_image  = "nginx:alpine"
  tags                      = var.tags
  api_target_group_arn      = module.alb.api_target_group_arn
  frontend_target_group_arn = module.alb.frontend_target_group_arn
}