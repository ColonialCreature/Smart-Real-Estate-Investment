
import os
import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

# Load enhanced dataset
df = pd.read_csv("real_estate.csv")

st.set_page_config(page_title="Smart City Explorer", layout="wide")
st.title("🏙️ Smart City Explorer")

# Sidebar - Location Filters
st.sidebar.header("📍 Location Selection")
states = sorted(df["State"].dropna().unique())
selected_state = st.sidebar.selectbox("Select State", states)

cities = sorted(df[df["State"] == selected_state]["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", cities)

zipcodes = df[(df["State"] == selected_state) & (df["City"] == selected_city)]["Correct_ZipCode"].dropna().unique()
zipcodes = sorted(map(str, zipcodes))
selected_zip = st.sidebar.selectbox("Select ZIP Code", ["All"] + zipcodes)

# Sidebar - Property Filters
st.sidebar.header("🏠 Property Filters")
min_price = st.sidebar.slider("Min Price ($)", 1000, 2000000, 200000)
max_price = st.sidebar.slider("Max Price ($)", 1000, 2000000, 1000000)
min_beds = st.sidebar.slider("Min Bedrooms", 1, 6, 2)

home_types = ["All"] + list(df["HomeType"].dropna().unique())
selected_type = st.sidebar.selectbox("Home Type", home_types)

rent_or_buy_options = ["All"] + list(df["RentOrBuy"].dropna().unique())
selected_rentbuy = st.sidebar.selectbox("Listing Type", rent_or_buy_options)

# Filter dataset
filtered = df[(df["State"] == selected_state) & (df["City"] == selected_city)]
if selected_zip != "All":
    filtered = filtered[filtered["Correct_ZipCode"].astype(str) == selected_zip]
filtered = filtered[
    (filtered["Price"] >= min_price) &
    (filtered["Price"] <= max_price) &
    (filtered["Bedrooms"] >= min_beds)
]
if selected_type != "All":
    filtered = filtered[filtered["HomeType"] == selected_type]
if selected_rentbuy != "All":
    filtered = filtered[filtered["RentOrBuy"] == selected_rentbuy]

# Main View
st.subheader(f"📊 Listings in {selected_city}, {selected_state} ({'ZIP ' + selected_zip if selected_zip != 'All' else 'All ZIPs'})")
if not filtered.empty:
    st.write(f"Showing {len(filtered)} listings.")
    st.dataframe(filtered[[
        "Address", "City", "State", "Correct_ZipCode", "RentOrBuy", "HomeType", "Price", "Size", "Bedrooms",
        "Bathroom", "LotSize", "GarageSize", "Pool", "Fireplace", "Basement", "YearBuilt",
        "DaysOnMarket", "EstimatedValue", "PricePerSqFt", "WalkScore", "TransitScore",
        "SchoolRating", "CrimeIndex"
    ]].head(50))

    # Chart: Price comparison by HomeType
    st.subheader("💹 Price Distribution by Home Type")
    st.bar_chart(filtered.groupby("HomeType")["Price"].mean().sort_values())

else:
    st.warning("No listings found for the selected filters.")

# Nearby Restaurants
st.subheader("📍 Nearby Restaurants")
def fetch_places_by_zip(zipcode):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": FOURSQUARE_API_KEY}
    params = {
        "near": zipcode,
        "limit": 5,
        "categories": "13065"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

zip_for_search = selected_zip if selected_zip != "All" else f"{selected_city}, {selected_state}"
places = fetch_places_by_zip(zip_for_search)
if places:
    for place in places:
        name = place["name"]
        address = place["location"].get("formatted_address", "N/A")
        st.markdown(f"**{name}**  \n{address}")
else:
    st.info("No restaurant data found for the selected location.")

# Chicago-only Crime Data
if selected_city.lower() == "chicago":
    st.subheader("🛑 Chicago Crime Snapshot (Latest 5 Incidents)")
    crime_data_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    params = {
        "$limit": 5,
        "$order": "date DESC"
    }
    response = requests.get(crime_data_url, params=params)
    if response.status_code == 200:
        crimes = response.json()
        for c in crimes:
            st.write(f"{c['date']} - {c['primary_type']} at {c.get('block', 'N/A')}")


# 🌤️ Weather Snapshot using Open-Meteo API
st.subheader("🌤️ Current Weather (Based on City)")

city_coords = {
    "chicago": (41.8781, -87.6298),
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "seattle": (47.6062, -122.3321),
    "houston": (29.7604, -95.3698),
    "denver": (39.7392, -104.9903),
    "philadelphia": (39.9526, -75.1652),
    "phoenix": (33.4484, -112.0740),
    "san antonio": (29.4241, -98.4936),
    "san diego": (32.7157, -117.1611),
    "dallas": (32.7767, -96.7970),
    "san jose": (37.3382, -121.8863),
    "austin": (30.2672, -97.7431),
    "jacksonville": (30.3322, -81.6557),
    "fort worth": (32.7555, -97.3308),
    "columbus": (39.9612, -82.9988),
    "charlotte": (35.2271, -80.8431),
    "san francisco": (37.7749, -122.4194),
    "indianapolis": (39.7684, -86.1581),
    "washington": (38.9072, -77.0369)
}

def fetch_weather(city):
    lat_lon = city_coords.get(city.lower())
    if not lat_lon:
        return {"Error": "City not supported for weather data."}
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat_lon[0],
            "longitude": lat_lon[1],
            "current_weather": "true",
            "timezone": "auto"
        }
        response = requests.get(url, params=params)
        data = response.json().get("current_weather", {})
        if not data:
            return {"Error": "No weather data returned."}
        condition_map = {
            0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
            55: "Dense drizzle", 61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Snow", 80: "Rain showers", 95: "Thunderstorm"
        }
        return {
            "Time": data.get("time"),
            "Temperature": f"{round((data.get('temperature', 0) * 9/5) + 32)}°F",
            "Windspeed": f"{round(data.get('windspeed', 0) * 0.621371)} mph",
            "Condition": condition_map.get(data.get("weathercode", 0), "Unknown")
        }
    except Exception as e:
        return {"Error": str(e)}

weather = fetch_weather(selected_city)
for k, v in weather.items():
    st.write(f"**{k}**: {v}")
