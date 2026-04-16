output "ecr_repository_names" {
  value = module.ecr.repository_names
}

output "ecr_repository_urls" {
  value = module.ecr.repository_urls
}
output "ecs_cluster_name" {
  value = module.ecs.cluster_name
}

output "ecs_api_service_name" {
  value = module.ecs.api_service_name
}

output "ecs_frontend_service_name" {
  value = module.ecs.frontend_service_name
}