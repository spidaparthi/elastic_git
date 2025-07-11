# GoldenGate Replication CI/CD

This directory contains utilities and CI/CD configuration for onboarding new Oracle tables to GoldenGate replication. Merge requests should update `tables/tables-to-replicate.yaml` with tables and pods to replicate. The GitLab pipeline validates YAML formatting, checks for duplicates, computes new tables, and verifies that tables exist in Oracle.

## Directory Layout

- `tables/tables-to-replicate.yaml` – list of tables to replicate
- `schemas/table_schema.json` – JSON schema for the YAML file
- `scripts/` – helper validation scripts
- `tests/` – test files

## Pipeline Overview

1. **YAML Linting** – enforced by `.yamllint`
2. **Schema Validation** – ensures required fields are present
3. **Duplicate Checks** – avoids table duplication
4. **Delta Detection** – writes new tables to `new_tables.txt`
5. **DB Validation** – confirms tables exist in the Oracle database

Credentials for Oracle should be provided through environment variables `ORACLE_USER`, `ORACLE_PASSWORD`, and `ORACLE_DSN` in the CI/CD settings.
