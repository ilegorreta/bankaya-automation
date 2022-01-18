terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  cloud {
    organization = "ilegorreta_personal"

    workspaces {
      name = "gh-actions-bankaya-test"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}
