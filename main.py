from opencage.geocoder import OpenCageGeocode
import folium
def get_location_from_opencage(address):
    api_key = "f808c7779f8948d18896a99cc53dd3cb"
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(address)
    if results:
        location = results[0]['geometry']
        return location['lat'], location['lng']
    return None, None

number = input("Enter phone number with country code:")
# ... (parse phone number and get location description as before)
number_location = "Burundi"  # For demonstration purposes

lat, lng = get_location_from_opencage(number_location) if number_location else (None, None)

if lat and lng:
    print("Latitude:", lat)
    print("Longitude:", lng)

    map_location = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=number_location).add_to(map_location)
    map_location.save("mylocation.html")
else:
    print("Could not find location coordinates.")
