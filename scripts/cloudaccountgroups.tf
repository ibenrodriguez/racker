# example code to iterate through lists and build trees
terraform {
  required_providers {
    prismacloud = {
      source = "PaloAltoNetworks/prismacloud"
      version = "1.1.5"
    }
  }
}

provider "prismacloud" {
  # Configuration options
}
variable	"cloudlist": {
    description = "Create Cloud Account Groups with these names"
    type        = list(string)
    default     = ["gcp", "aws", "az", "oci"]
}
variable	"bizunit": {
    description = "Create Cloud Account Groups with these names"
    type        = list(string)
    default     = ["crp", "eng", "spt", "mkt", "sls", "int"]
}
variable	"tier": {
    description = "Create Cloud Account Groups with these names"
    type        = list(string)
    default     = ["brz", "slv", "gld", "plt"]
}

var.lists.cloudlist #iterate through and create an account group for each item in cloudlist
resource "prismacloud_account_group" "Clouds" {
    count = length(var.cloudlist)
    name = var.cloudlist[count.index]
    description = "Made by Terraform - see ADO repo for code"
    child_group_ids var.bizunit
}

var.lists.cloudlist #iterate through and create an account group for each item in cloudlist
resource "prismacloud_account_group" "Clouds" {
    count = length(var.cloudlist)
    name = var.cloudlist[count.index]
    description = "Made by Terraform - see ADO repo for code"
    child_group_ids var.tier
}

