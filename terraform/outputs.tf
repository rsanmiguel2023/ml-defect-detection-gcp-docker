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

output "storage_bucket_name" {
  description = "Cloud Storage bucket"

  value = google_storage_bucket.ml_storage.name
}

output "storage_bucket_url" {
  description = "Cloud Storage URL"

  value = google_storage_bucket.ml_storage.url
}

output "cloud_run_service_account_email" {
  description = "Cloud Run service account email"
  value       = google_service_account.cloud_run_service_account.email
}

output "cloud_run_service_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_v2_service.ml_defect_api.uri
}