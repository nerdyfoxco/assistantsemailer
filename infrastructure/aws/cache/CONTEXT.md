# Chapter 06: Cache (Redis)

## Purpose
To provide high-speed, in-memory caching for the application using AWS ElastiCache (Redis).

## Context
"Phase 1: Infrastructure."
The "Brain" and "Connectors" need a shared state layer for:
- Job queues (BullMQ/Sidekiq patterns).
- Hot data caching (User sessions, recent emails).
- Rate limiting counters.

## Requirements
1.  **Elasticache Replication Group**: "assistants-redis".
2.  **Engine**: Redis 7.0+.
3.  **Subnet Group**: Private subnets.
4.  **Security Group**: Allow access from EKS/Lambda.

## Verification
1.  `terraform validate`.
2.  Visual Report showing Replication Group Status and Engine Version.
