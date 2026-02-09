# Chapter 04: Compute (EKS/Lambda)

## Purpose
To provide the execution environments for Containerized Microservices (EKS) and Event-Driven Functions (Lambda).

## Context
"Phase 1: Infrastructure."
We need a Kubernetes Cluster for the core "Brain" and "Connectors", and Lambda for lightweight glue code.

## Requirements
1.  **EKS Cluster**: "assistants-cluster".
2.  **Node Group**: Managed Node Group for workers.
3.  **Lambda**: Placeholder for "EventProcessor".

## Verification
1.  `terraform validate`.
2.  Visual Report showing Cluster Status and Node Group config.
