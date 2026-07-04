#
# Outputs
#

output "artifact_registry_repository" {
  description = "Artifact Registry repository name"
  value       = google_artifact_registry_repository.docker_repository.name
}

output "artifact_registry_location" {
  description = "Artifact Registry repository location"
  value       = google_artifact_registry_repository.docker_repository.location
}