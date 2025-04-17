# File Name: apiHandler.py
# Student Name: Collin Baines / Vanshika Rana
# email: bainesct@mail.uc.edu / ranava@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 04/17/2025
# Course #/Section: IS4010-002
# Semester/Year: Spring/2025
# Brief Description of the assignment: This assignment requires us to manipulate data within csv files and retrieve information from a given API.

# Brief Description of what this module does. This module connects us to the API and retrieves data from it.
# Citations: ChatGPT

# Anything else that's relevant:

import requests

class ZipCodeAPIClient:
    def __init__(self):
        self.api_key = "fb90b3e0-1a6b-11f0-ae1c-675bedbafc10"
        self.base_url = "https://app.zipcodebase.com/api/v1/search"

    def get_zip(self, city, state):
        try:
            url = "https://app.zipcodebase.com/api/v1/code/city"
            params = {
                "apikey": self.api_key,
                "city": city,
                "state": state,
                "country": "US"
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and isinstance(data['results'], list) and data['results']:
                    # Each item in data['results'] is just a string (the zip)
                    return data['results'][0]  # Just return the string
                else:
                    print(f"No results for {city}, {state}")
            else:
                print(f"API failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"API error for {city}, {state}: {e}")
        return None










