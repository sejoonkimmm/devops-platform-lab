# Task 4 — Weekly business report

Every Monday the product manager pulls a few business numbers from the database by
hand. `weekly_report.py` does that run, writes one CSV per ISO week, and the business
reporting tool picks the file up. No Grafana involved.

Files:
- `weekly_report.py` — the job. Reads the metrics, writes `weekly_metrics_<year>_W<week>.csv`.
- `reporting-role.sql` — the read-only database role the job uses.
- `cronjob.yaml` — runs it every Monday on the cluster.
- `Dockerfile`, `requirements.txt` — build the job image.

## Credentials

Today the manager uses the application's own database user. That is the main problem here.

- That user can read and write every table and change the schema. A report only needs
  to read three tables. If the credential leaks, the whole database is exposed.
- App traffic and report traffic share one login, so you cannot tell them apart in an
  audit or a slow-query log.
- The credential cannot be rotated on its own. Rotating it to contain a leak also
  restarts or breaks the application.

Better: a dedicated `reporting` role with `SELECT` only on the three tables it reads
(`reporting-role.sql`). Its password lives in a secret manager (Vault or the cloud
secret store), is delivered to the job as a Kubernetes Secret through External Secrets,
and is rotated on its own schedule. The application user is never used for reporting.

## Scheduling

A Kubernetes CronJob at `0 6 * * 1` (Monday 06:00). It runs on the same platform we
already operate, so it is logged, retried and visible next to everything else. A cron
line on someone's laptop or a single VM would be a single point of failure with no
history when it silently stops.

## Keeping it from becoming new toil

- The database query is retried up to three times with a wait between tries, so a brief
  blip does not fail the run.
- `connect_timeout` plus the retries mean a database that is down fails fast and loud
  instead of hanging.
- On a hard failure the job posts to an alert webhook and exits non-zero, so a bad run
  pages someone instead of passing in silence.
- `concurrencyPolicy: Forbid` stops two runs from overlapping. `backoffLimit` and
  `activeDeadlineSeconds` bound the retries and runtime.
- The output file is keyed by ISO week, so re-running the same week overwrites the same
  file instead of creating duplicates.
- `failedJobsHistoryLimit` keeps the last failed pods around so you can read the logs.

## Run it

```bash
# one time: create the read-only role
psql -h <db-host> -U <admin> -d springboot_demo -f reporting-role.sql

# secret with the reporting credential (in real use: External Secrets from Vault)
kubectl -n pricing create secret generic report-db \
  --from-literal=REPORT_DB_HOST=postgres \
  --from-literal=REPORT_DB_NAME=springboot_demo \
  --from-literal=REPORT_DB_USER=reporting \
  --from-literal=REPORT_DB_PASSWORD=<from-secret-manager> \
  --from-literal=ALERT_WEBHOOK_URL=<slack-or-teams-webhook>

kubectl apply -f cronjob.yaml
```
