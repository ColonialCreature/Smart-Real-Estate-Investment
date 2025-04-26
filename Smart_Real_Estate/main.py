
import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from real_estate_service import RealEstateService

# Load environment variables
load_dotenv()

# API Keys from .env
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

# Initialize real estate service
real_estate = RealEstateService("real_estate.csv")

def get_real_estate_summary(city):
    print("\n🏡 Real Estate Summary")
    summary = real_estate.summarize_by_city(city)
    if isinstance(summary, dict):
        for k, v in summary.items():
            print(f"{k}: {v}")
    else:
        print(summary)

def get_chicago_crime_data():
    print("\n🛑 Crime Data for Chicago (Sample)")
    url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    params = {
        "$limit": 5,
        "$order": "date DESC"
    }
    response = requests.get(url, params=params)
    crimes = response.json()
    for c in crimes:
        print(f"{c['date']} - {c['primary_type']} at {c.get('block', 'N/A')}")

def get_places_from_foursquare(city):
    print("\n📍 Places of Interest from Foursquare")
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": FOURSQUARE_API_KEY
    }
    params = {
        "near": city,
        "limit": 5,
        "categories": "13065"  # Restaurants
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    for place in data.get("results", []):
        print(f"{place['name']} - {place['location'].get('formatted_address', 'N/A')}")

def get_census_data(state_fips="17", county_fips="031"):
    print("\n👥 Census Demographics (Cook County, IL)")
    url = f"https://api.census.gov/data/2020/pep/population"
    params = {
        "get": "NAME,POP,DATE_CODE",
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}",
        "key": CENSUS_API_KEY
    }
    response = requests.get(url, params=params)
    try:
        data = response.json()
        headers = data[0]
        values = data[1]
        for h, v in zip(headers, values):
            print(f"{h}: {v}")
    except Exception as e:
        print("Error fetching census data:", e)

def main():
    while True:
        print("\n====== Smart City Explorer ======")
        print("1. Real Estate Summary")
        print("2. Chicago Crime Snapshot")
        print("3. Places of Interest (Foursquare)")
        print("4. US Census Population Stats")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            city = input("Enter city (e.g., Chicago, IL): ")
            get_real_estate_summary(city)
        elif choice == "2":
            get_chicago_crime_data()
        elif choice == "3":
            city = input("Enter city for POIs (e.g., Chicago, IL): ")
            get_places_from_foursquare(city)
        elif choice == "4":
            get_census_data()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
