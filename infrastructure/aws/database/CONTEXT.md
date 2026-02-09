# Chapter 05: Database (RDS)

## Purpose
To provide persistent relational storage (PostgreSQL) for the application.

## Context
"Phase 1: Infrastructure."
The "Brain" service needs a reliable place to store long-term memory (embeddings, user data) via vector extensions or JSONB, though this chapter focuses on the infrastructure itself.

## Requirements
1.  **RDS Instance**: Postgres 15+ "assistants-db".
2.  **Subnet Group**: Private subnets for the DB.
3.  **Security Group**: Allow access from EKS/Lambda (placeholder for now, or referenced).

## Verification
1.  `terraform validate`.
2.  Visual Report showing DB Instance and Engine version.
