variable "project" {
  default = "focus-poet-376519"
}

variable "service_account_id" {
  default = "dbt-service-account"
}

variable "service_account_display_name" {
  default = "dbt-service-account"
}

variable "bucket_name" {
  default = "dbt-bucket-de-zoomcamp"
}

variable "big-query-tables" {
  type = list(any)
  default = ["green_tripdata", "yellow_tripdata", "green_trip_data_2021_01", "green_trip_data_2021_02",
    "green_trip_data_2021_03", "green_trip_data_2021_04", "yellow_trip_data_2021_01",
  "yellow_trip_data_2021_02", "yellow_trip_data_2021_03", "yellow_trip_data_2021_04"]
}

variable "location" {
  default = "US"
}
