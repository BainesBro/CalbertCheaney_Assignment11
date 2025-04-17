# File Name: main.py
# Student Name: Collin Baines / Vanshika Rana
# email: bainesct@mail.uc.edu / ranava@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 04/17/2025 
# Course #/Section: IS4010-002
# Semester/Year: Spring/2025
# Brief Description of the assignment: This assignment requires us to manipulate data within csv files and retrieve information from a given API.

# Brief Description of what this module does. This module calls upon the functions made in cleaner.py and apiHandler.py
# Citations: ChatGPT

# Anything else that's relevant:

from dataProcessing.cleaner import FuelDataCleaner

def main():
    cleaner = FuelDataCleaner("Data/fuelPurchaseData.csv")
    cleaner.process_data()

if __name__ == "__main__":
    main()
