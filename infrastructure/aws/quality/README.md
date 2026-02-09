# Chapter 08: Quality (CI/CD)

## Purpose
To enforce infrastructure quality and automation via GitHub Actions.

## Context
"Phase 1: Infrastructure."
- **CI/CD**: Automates `terraform plan` and `terraform apply`.
- **Quality**: Ensures code formatting (`terraform fmt`) and validation (`terraform validate`) before merge.

## Requirements
1.  **Workflow**: `.github/workflows/terraform.yml`.
2.  **Triggers**: Push to `main`, Pull Request to `main`.
3.  **Jobs**: `Plan` (on PR), `Apply` (on Push to main).

## Verification
1.  Verify `.github/workflows/terraform.yml` exists and is valid YAML.
2.  Visual Report showing Workflow Definition.
