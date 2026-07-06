locals {

  common_labels = {
    project     = "ml-defect-detection"
    managed_by  = "terraform"
    environment = var.environment
  }

}