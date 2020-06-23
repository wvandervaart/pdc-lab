from nbrestlib import NBRestConnection

import json

token = ""
nbhost = "netbox"

def main():
    nbconn = NBRestConnection(nbhost, token)
    # Define the supernet
    prefix = "fc00::/48"
    # Get the prefix-id for the supernet
    prefix_id = nbconn.api_get_prefixid(prefix)

    print(prefix_id)

if __name__ == "__main__":
    main()

