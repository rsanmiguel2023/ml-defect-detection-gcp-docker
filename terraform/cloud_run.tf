#
# Cloud Run resources
#
resource "google_cloud_run_v2_service" "ml_defect_api" {
  name     = var.cloud_run_service_name
  project  = var.project_id
  location = var.region

  template {
    service_account = google_service_account.cloud_run_service_account.email

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repository}/ml-defect-api:latest"

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
      }
    }

    timeout = "300s"
  }

  depends_on = [
    google_project_service.required_services,
    google_artifact_registry_repository.docker_repository,
    google_service_account.cloud_run_service_account,
  ]

  labels = local.common_labels
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.ml_defect_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}