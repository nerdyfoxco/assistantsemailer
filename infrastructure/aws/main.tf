provider "aws" {
  region = var.aws_region
}

resource "aws_organizations_organization" "root" {
  feature_set = "ALL"
  enabled_policy_types = [
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY"
  ]
}

resource "aws_organizations_organizational_unit" "workloads" {
  name      = "Workloads"
  parent_id = aws_organizations_organization.root.roots[0].id
}
