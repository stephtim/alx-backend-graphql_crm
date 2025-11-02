#!/usr/bin/env python3
# crm/cron_jobs/send_order_reminders.py
"""
Query local GraphQL endpoint for orders in the last 7 days and log reminders.
Logs appended to /tmp/order_reminders_log.txt with timestamp.
Prints "Order reminders processed!" to console.
"""

from datetime import datetime, timezone, timedelta
import os
import sys
import json

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Absolute log path (best practice)
LOG_FILE = "/tmp/order_reminders_log.txt"

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Build transport and client
transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3, timeout=10)
client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL query: fetch recent orders (we'll filter client-side to avoid depending on server filters)
QUERY = gql(
    """
    query {
      allOrders(first: 100) {
        edges {
          node {
            id
            orderDate
            customer {
              email
            }
          }
        }
      }
    }
    """
)

def parse_iso(dt_str):
    if not dt_str:
        return None
    # handle trailing Z (UTC) if present
    try:
        if dt_str.endswith("Z"):
            dt_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(dt_str)
    except Exception:
        # fallback: try basic parse
        try:
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            return None

def main():
    try:
        # run query
        result = client.execute(QUERY)
        edges = result.get("allOrders", {}).get("edges", [])
        now = datetime.now(timezone.utc)
        seven_days_ago = now - timedelta(days=7)

        processed = 0
        lines = []
        for edge in edges:
            node = edge.get("node") or {}
            order_id = node.get("id")
            order_date_raw = node.get("orderDate")
            customer = node.get("customer") or {}
            email = customer.get("email") or "no-email"

            order_dt = parse_iso(order_date_raw)
            # if unable to parse, skip
            if not order_dt:
                continue

            # normalize to timezone-aware UTC if naive
            if order_dt.tzinfo is None:
                order_dt = order_dt.replace(tzinfo=timezone.utc)

            if order_dt >= seven_days_ago:
                timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
                line = f"{timestamp} - Order ID: {order_id} - Customer Email: {email}"
                lines.append(line)
                processed += 1

        # Append lines to log atomically
        if lines:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                for ln in lines:
                    f.write(ln + os.linesep)

        # Always print final message (required)
        print("Order reminders processed!")

    except Exception as exc:
        # log exception to the same log file with timestamp
        err_ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{err_ts} - ERROR during order reminders: {repr(exc)}{os.linesep}")
        # reprint summary to console
        print("Order reminders processed! (with errors)")
        # also exit non-zero so cron callers can detect failures if needed
        sys.exit(1)

if __name__ == "__main__":
    main()
