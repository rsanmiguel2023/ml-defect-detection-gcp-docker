#
# IAM resources
#
resource "google_service_account" "cloud_run_service_account" {
  project      = var.project_id
  account_id   = "ml-defect-cloud-run"
  display_name = "ML Defect Detection Cloud Run Service Account"
  description  = "Service account used by the Cloud Run inference service."
}

resource "google_project_iam_member" "cloud_run_storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

resource "google_project_iam_member" "cloud_run_artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}