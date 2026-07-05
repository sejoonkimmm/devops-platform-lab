# Task 4: Weekly business report

Every Monday the product manager pulls a few business numbers from the database by
hand. `weekly_report.py` does that run, writes one CSV per ISO week, and the business
reporting tool picks the file up. No Grafana involved. The reasoning (credentials,
scheduling, keeping it from becoming toil) lives in the writeup; this folder holds
the working parts.

Files:
- `weekly_report.py` is the job. It reads the metrics and writes `weekly_metrics_<year>_W<week>.csv`.
- `reporting-role.sql` creates the read-only database role the job uses.
- `cronjob.yaml` runs it every Monday on the cluster.
- `Dockerfile` and `requirements.txt` build the job image.

## Run it

```bash
# build and push the job image (pinned tag; the cronjob pulls this)
docker build -t ghcr.io/sejoonkimmm/weekly-report:1.0.0 .
docker push ghcr.io/sejoonkimmm/weekly-report:1.0.0

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
