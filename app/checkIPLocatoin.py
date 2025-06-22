#!/usr/bin/python3

import requests
import json

def get_ip_location():
    try:
        # Get public IP address
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_data = ip_response.json()
        ip_address = ip_data['ip']
        
        # Get location information using ip-api.com
        location_response = requests.get(f'http://ip-api.com/json/{ip_address}')
        location_data = location_response.json()
        
        if location_data['status'] == 'success':
            print("\nLocation Information:")
            print(f"IP Address: {ip_address}")
            print(f"City: {location_data.get('city', 'N/A')}")
            print(f"Region: {location_data.get('regionName', 'N/A')}")
            print(f"Country: {location_data.get('country', 'N/A')}")
            print(f"Country Code: {location_data.get('countryCode', 'N/A')}")
            print(f"ISP: {location_data.get('isp', 'N/A')}")
            print(f"Latitude: {location_data.get('lat', 'N/A')}")
            print(f"Longitude: {location_data.get('lon', 'N/A')}")
        else:
            print("Failed to retrieve location information.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    except KeyError as e:
        print(f"Missing expected data in response: {e}")

if __name__ == "__main__":
    print("Fetching your IP address location...")
    get_ip_location()