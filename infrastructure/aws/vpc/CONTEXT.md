# Chapter 02: Network (VPC)

## Purpose
To create the isolated network environment where all subsequent workloads (EKS, RDS, Lambda) will reside.

## Context
"Phase 1: Infrastructure."
The VPC is the literal ground we walk on in AWS.

## Requirements
1.  **VPC**: 10.0.0.0/16.
2.  **Subnets**: Public (ALB) and Private (Apps/Data).
3.  **Gateways**: IGW for Public, NAT for Private.
4.  **AZs**: Multi-AZ (3 zones) for HA.
5.  **Flow Logs**: Enabled for Audit.

## Verification
1.  `terraform validate`.
2.  Visual Report showing subnet map and route table logic.
