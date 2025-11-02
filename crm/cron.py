import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Set up logging
LOG_FILE = "/tmp/crm_heartbeat_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(message)s")

def log_crm_heartbeat():
    """
    Logs CRM heartbeat and checks GraphQL hello endpoint using gql.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"
    
    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    # Set up the GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    # Create GraphQL client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query
    query = gql(
        """
        query {
            hello
        }
        """
    )

    try:
        response = client.execute(query)
        logging.info(f"{timestamp} GraphQL hello response: {response}")
        print("GraphQL hello response:", response)
    except Exception as e:
        error_message = f"{timestamp} Error connecting to GraphQL: {e}"
        logging.error(error_message)
        print(error_message)
