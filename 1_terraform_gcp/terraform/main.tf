terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.18.0"
    }
  }
}

provider "google" {
  credentials = "./keys/credk.json"
  project     = "my-de-journey"
  region      = "africa-south1-a"
}



resource "google_storage_bucket" "my-de-journey-bucket" {
  name          = "olalekan-de2753-bucket"
  location      = "africa-south1"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}