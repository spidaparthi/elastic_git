# Goldengate Automation

This directory contains scripts and configuration used to automate the
addition of tables to Oracle Goldengate running on EC2. The workflow is
executed through GitLab CI/CD and performs validation, testing and
deployment of new tables.

## Directory layout

- `tables/` – YAML files submitted by users with new tables.
- `scripts/` – helper scripts used by the CI/CD pipeline.
- `state/` – files tracking replicated tables.

## Pipeline overview

1. **Validation and tests** – triggered for merge request pipelines.
   - Lints YAML files and validates their schema.
   - Verifies that a table is not already replicated.
   - Optionally checks the table exists in the database.
   - Spins up a Goldengate container and validates deployment.
2. **Deploy** – runs on the default branch after merge.
   - Updates extract and replicat include files.
   - Restarts Goldengate processes and verifies they are running.

Two merge request approvals are required in GitLab before merging. The
`deploy` job runs only after the merge request pipeline and approvals
succeed.
