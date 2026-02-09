# Chapter 03: Identity (IAM)

## Purpose
To define the Principle of Least Privilege for all Cloud Resources.

## Context
"Phase 1: Infrastructure."
Identity is the new perimeter. we need Roles for EKS (Cluster/Node), Lambda (Execution), and basic Admin.

## Requirements
1.  **EKS Cluster Role**: Allow EKS to manage resources.
2.  **EKS Node Role**: Allow Worker Nodes to join cluster.
3.  **Lambda Basic**: Allow logging to CloudWatch.
4.  **Admin**: (Optional/Placeholder for future use).

## Verification
1.  `terraform validate`.
2.  Visual Report showing Role/Policy mapping.
