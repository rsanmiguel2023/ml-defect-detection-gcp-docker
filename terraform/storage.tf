#
# Cloud Storage resources
#
resource "google_storage_bucket" "ml_storage" {

  name     = var.storage_bucket_name
  project  = var.project_id
  location = var.region

  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  public_access_prevention = "enforced"

  versioning {
    enabled = true
  }

  lifecycle_rule {

    action {
      type = "Delete"
    }

    condition {
      age = 90
    }
  }

  labels = local.common_labels

  depends_on = [
    google_project_service.required_services
  ]
}