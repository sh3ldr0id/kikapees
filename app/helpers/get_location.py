from requests import get

def get_location(ip_address):
    try:
        response = get(f'https://api.iplocation.net/?ip={ip_address}').json()

        location_data = {
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
            
        }
    except:
        location_data = {}

    return location_data