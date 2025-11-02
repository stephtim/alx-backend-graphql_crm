import datetime
import requests

def log_crm_heartbeat():
    """Logs a timestamped heartbeat message and optionally checks GraphQL hello."""
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Append log
    with open(log_file, "a") as f:
        f.write(message)

    # Optional: verify GraphQL endpoint responsiveness
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok:
            print("GraphQL hello response:", response.json())
        else:
            print("GraphQL endpoint not responding properly.")
    except Exception as e:
        print("Error checking GraphQL:", e)
