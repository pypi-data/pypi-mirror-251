# ensembl_variants_lookup/utils/variant_helpers.py
import requests
import pandas as pd

def get_variants_by_rsid(rsid):
    # Set the url/endpoint provided by Ensembl database
    server = "https://rest.ensembl.org/variation/human/"
    
    # Add the rsid for the SNP of interest
    extension = f"{rsid}?"
    
    # Add the extension/rsid to complete the endpoint
    full_url = server + extension

    # Provide Content Type
    result = requests.get(full_url, headers={"Content-Type": "application/json"})
    
    # Check the request http status
    result.raise_for_status()

    return result.json()

def get_variants_by_rsid_list(variant_ids):
    server = "https://rest.ensembl.org"
    endpoint = "/variation/human"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"ids": variant_ids}

    try:
        response = requests.post(server + endpoint, headers=headers, json=payload)
        response.raise_for_status()
        decoded = response.json()
        
        # Create a DataFrame from the decoded JSON response
        df = pd.DataFrame(decoded)
        
        # Print the DataFrame
        print(df)

        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching variant data: {e}")
        return None
