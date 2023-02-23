terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "focus-poet-376519"
}

resource "google_service_account" "service_account" {
    account_id = "dbt-service-account"
    display_name = "dbt-service-account"
    description = "Service account for dbt cloud"
}

