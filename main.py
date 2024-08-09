import pygeoip

GEOIP_DATABASE_PATH = 'GeoLiteCity.dat'
gi = pygeoip.GeoIP(GEOIP_DATABASE_PATH)

def TargetIP(ip_address):
    try:
        rec = gi.record_by_name(ip_address)
        if rec:
            city = rec.get('city', 'Unknown')
            country = rec.get('country_name', 'Unknown')
            lng = rec.get('longitude', 'Unknown')
            lat = rec.get('latitude', 'Unknown')
            print(f"City: {city}")
            print(f"Country: {country}")
            print(f"Longitude: {lng}")
            print(f"Latitude: {lat}")
        else:
            print("No data found for the IP address.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Exemple d'adresse IP
ip_address = input("Enter IP address: ")
TargetIP(ip_address)