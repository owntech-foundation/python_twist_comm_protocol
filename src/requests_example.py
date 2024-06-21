import requests

# Replace with your NREL API key
api_key = ' 3EC5Q2iQOwsvQBFRcvs8e8Hb6Nhpb21ExoyRy6QF '

# Dictionary with coordinates for New York, Paris, and Toulouse
coordinates = {
    'New York': {
        'latitude': 40.7128,
        'longitude': -74.0060
    },
    'Paris': {
        'latitude': 48.8566,
        'longitude': 2.3522
    },
    'Toulouse': {
        'latitude': 43.6047,
        'longitude': 1.4442
    }
}

# Function to get irradiance data for a given location
def get_irradiance(api_key, lat, lon):
    url = f"https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={api_key}&lat={lat}&lon={lon}"
    response = requests.get(url)
    data = response.json()

    if 'outputs' in data:
        return data['outputs']['avg_ghi']
    else:
        return None

# Loop through each location and get irradiance data
for city, coords in coordinates.items():
    irradiance = get_irradiance(api_key, coords['latitude'], coords['longitude'])
    if irradiance is not None:
        print(f"{city} - Global Horizontal Irradiance: {irradiance} W/m²")
    else:
        print(f"{city} - Irradiance information is not available.")
