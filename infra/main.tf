terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

# IAM Service Account - BigQuery Admin
provider "google" {
  project = var.project
}

resource "google_service_account" "service_account" {
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
  description  = "Service account for dbt cloud"
}

resource "google_project_iam_member" "my_service_account_roles" {
  project = var.project
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_key" "my_service_account_key" {
  service_account_id = google_service_account.service_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

output "my_service_account_key_json" {
  value     = google_service_account_key.my_service_account_key.private_key
  sensitive = true
}

#Cloud Storage Buckets
resource "google_storage_bucket" "de-zoomcamp-bucket" {
  name     = var.bucket_name
  location = var.location
}

#BigQuery datasets
resource "google_bigquery_dataset" "dbt-dataset-maria" {
  dataset_id = "dbt_maria"
  location   = var.location
}

resource "google_bigquery_dataset" "dbt-dataset-production" {
  dataset_id = "production"
  location   = var.location
}

resource "google_bigquery_dataset" "dbt-dataset-staging" {
  dataset_id = "staging"
  location   = var.location
}

resource "google_bigquery_dataset" "dbt-dataset-trips-data" {
  dataset_id = "trips_data_all"
  location   = var.location
}

#BigQuery tables
resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.dbt-dataset-trips-data.dataset_id
  count      = length(var.big-query-tables)
  table_id   = var.big-query-tables[count.index]
}
