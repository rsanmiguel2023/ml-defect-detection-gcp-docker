#
# Artifact Registry resources
#

resource "google_artifact_registry_repository" "docker_repository" {
  project       = var.project_id
  location      = var.region
  repository_id = var.artifact_registry_repository
  description   = "Docker images for ML defect detection platform"
  format        = "DOCKER"

  labels = local.common_labels

  depends_on = [
    google_project_service.required_services
  ]
}