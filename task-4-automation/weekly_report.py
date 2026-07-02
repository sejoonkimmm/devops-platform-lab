"""Weekly business metrics export for the pricing service. Runs as a Monday CronJob."""

import csv
import json
import os
import sys
import time
import urllib.request
from datetime import date, datetime, timezone

import psycopg2

RETRIES = 3
RETRY_WAIT_SECONDS = 10

QUERIES = {
    "total_products": "SELECT count(*) FROM products",
    "active_prices": "SELECT count(*) FROM prices WHERE valid_until IS NULL OR valid_until > now()",
    "price_updates_last_7d": "SELECT count(*) FROM prices WHERE source <> 'SEED' AND created_at >= now() - interval '7 days'",
    "new_products_last_7d": "SELECT count(*) FROM products WHERE created_at >= now() - interval '7 days'",
    "messages_last_7d": "SELECT count(*) FROM messages WHERE created_at >= now() - interval '7 days'",
    "catalog_value_usd": "SELECT coalesce(sum(base_price), 0) FROM products",
}


def connect():
    return psycopg2.connect(
        host=os.environ["REPORT_DB_HOST"],
        port=os.environ.get("REPORT_DB_PORT", "5432"),
        dbname=os.environ["REPORT_DB_NAME"],
        user=os.environ["REPORT_DB_USER"],
        password=os.environ["REPORT_DB_PASSWORD"],
        connect_timeout=10,
    )


def collect(conn):
    metrics = {}
    with conn.cursor() as cur:
        for name, sql in QUERIES.items():
            cur.execute(sql)
            metrics[name] = cur.fetchone()[0]
    return metrics


def write_report(metrics, out_dir):
    iso_year, iso_week, _ = date.today().isocalendar()
    path = os.path.join(out_dir, f"weekly_metrics_{iso_year}_W{iso_week:02d}.csv")
    generated_at = datetime.now(timezone.utc).isoformat()
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "generated_at"])
        for name, value in metrics.items():
            writer.writerow([name, value, generated_at])
    return path


def alert(message):
    url = os.environ.get("ALERT_WEBHOOK_URL")
    if not url:
        return
    body = json.dumps({"text": f"[weekly-report] {message}"}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"alert delivery failed: {e}", file=sys.stderr)


def main():
    out_dir = os.environ.get("REPORT_OUTPUT_DIR", "/data/reports")
    os.makedirs(out_dir, exist_ok=True)
    last_error = None
    for attempt in range(1, RETRIES + 1):
        try:
            conn = connect()
            try:
                metrics = collect(conn)
            finally:
                conn.close()
            path = write_report(metrics, out_dir)
            print(f"wrote {path}: {metrics}")
            return 0
        except Exception as e:
            last_error = e
            print(f"attempt {attempt}/{RETRIES} failed: {e}", file=sys.stderr)
            if attempt < RETRIES:
                time.sleep(RETRY_WAIT_SECONDS)
    alert(f"failed after {RETRIES} attempts: {last_error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
