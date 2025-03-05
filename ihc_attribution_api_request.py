import requests
import json

# API URL and your API key
url = 'https://api.ihc-attribution.com/v1/compute_ihc?conv_type_id=conversiontype'
api_key = 'fefbddbb-146c-4389-9807-b451e36dc45b'

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

def post_compute_ihc(conv_id, journey):
    # Data payload
    data = {
        'customer_journeys': journey
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Print the response
    if response.status_code == 200:
        print('Data received from IHC.')
        value=response.json()["value"]
        return value
    else:
        print('Error:', response.status_code, response.text)
