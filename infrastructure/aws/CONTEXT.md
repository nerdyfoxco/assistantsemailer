# Chapter 01: AWS Organization

## Purpose
To establish the Root of Trust in the Cloud. The Organization account holds the master billing and security policies (SCPs).

## Context
"Phase 1: Infrastructure."
We need a clean slate AWS environment. Using Terraform locally to define it.

## Requirements
1.  **Provider**: AWS (us-east-1).
2.  **Resources**: `aws_organizations_organization`.
3.  **Validation**: `terraform validate` must pass.
4.  **Security**: No hardcoded credentials (use env vars).

## Verification
1.  `terraform init`
2.  `terraform validate`
3.  `terraform plan` -> Generate HTML Report.
