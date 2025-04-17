# File Name: cleaner.py
# Student Name: Collin Baines / 
# email: bainesct@mail.uc.edu /
# Assignment Number: Assignment 11
# Due Date: 04/17/2025
# Course #/Section: IS4010-002
# Semester/Year: Spring/2025
# Brief Description of the assignment: This assignment requires us to manipulate data within csv files and retrieve information from a given API.

# Brief Description of what this module does. This module corrects the Gross Price, deletes duplicates, and manipulates data from the API.
# Citations: ChatGPT

# Anything else that's relevant:

import pandas as pd
import os
import re
from dataProcessing.apiHandler import ZipCodeAPIClient

class FuelDataCleaner:
    def __init__(self, input_file):
        self.input_file = input_file
        self.api_client = ZipCodeAPIClient()
        self.data = pd.read_csv(self.input_file, dtype=str)

        # Format Gross Price
        self.data['Gross Price'] = self.data['Gross Price'].astype(float).round(2)

        # Extract City & State from Full Address
        self.data[['City', 'State']] = self.data['Full Address'].apply(self.extract_city_state)

        # Add Zip Code column if it's missing
        if 'Zip Code' not in self.data.columns:
            self.data['Zip Code'] = pd.NA

        print("Loaded columns:", self.data.columns.tolist())

    def extract_city_state(self, full_address):
        try:
            match = re.search(r',\s*([A-Za-z\s]+),\s*([A-Z]{2})\b', full_address)
            if match:
                city = match.group(1).strip()
                state = match.group(2).strip()
                return pd.Series([city, state])
        except:
            pass
        return pd.Series([pd.NA, pd.NA])

    def remove_duplicates(self):
        self.data = self.data.drop_duplicates()

    def separate_anomalies(self):
        anomalies = self.data[self.data['Fuel Type'].str.lower() == 'pepsi']
        self.data = self.data[self.data['Fuel Type'].str.lower() != 'pepsi']
        os.makedirs("Data", exist_ok=True)
        anomalies.to_csv("Data/dataAnomalies.csv", index=False)

    def fill_missing_zip_codes(self):
        # Only take rows missing a ZIP and with valid City and State
        candidates = self.data[self.data['Zip Code'].isna()]
        valid_rows = candidates[candidates['City'].notna() & candidates['State'].notna()].head(5)

        print("\nLooking up ZIP codes for these rows:")
        print(valid_rows[['Full Address', 'City', 'State']])

        for idx, row in valid_rows.iterrows():
            city = row['City']
            state = row['State']
            print(f"Looking up ZIP for: {city}, {state}")
            zip_code = self.api_client.get_zip(city, state)
            print(f"Got ZIP: {zip_code}")
            if zip_code:
                self.data.at[idx, 'Zip Code'] = zip_code

        print("\nUpdated ZIP codes in:")
        print(self.data.loc[valid_rows.index][['City', 'State', 'Zip Code']])


    def write_cleaned_data(self):
        self.data.to_csv("Data/cleanedData.csv", index=False)

    def process_data(self):
        print("Starting data processing...")
        self.remove_duplicates()
        print("Duplicates removed.")
        self.separate_anomalies()
        print("Anomalies written.")
        self.fill_missing_zip_codes()
        print("ZIP codes filled (up to 5).")
        self.write_cleaned_data()
        print("Cleaned data saved.")
