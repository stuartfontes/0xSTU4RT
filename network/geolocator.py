import geoip2.database
import geoip2.errors
import ipaddress
import socket

DB_PATH = "data/GeoLite2-City.mmdb"

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return None

def resolve_to_ip(target):
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            return None

def geolocate(target):
    ip = resolve_to_ip(target)

    if ip is None:
        return {"error": f"could not resolve '{target}' to an IP address"}

    if is_private_ip(ip):
        return {"error": "private/local IP, no geolocation available"}

    try:
        reader = geoip2.database.Reader(DB_PATH)
        response = reader.city(ip)
        reader.close()

        return {
            "ip": ip,
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }
    except geoip2.errors.AddressNotFoundError:
        return {"error": "IP not found in database"}
    except FileNotFoundError:
        return {"error": f"database file not found at {DB_PATH}"}