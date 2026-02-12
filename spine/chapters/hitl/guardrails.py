
import re
from urllib.parse import urlparse
import ipaddress
import socket

# Block private ranges (SSRF protection)
PRIVATE_RANGES = [
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),
    ipaddress.ip_network('0.0.0.0/8'),
    ipaddress.ip_network('224.0.0.0/4'),
    ipaddress.ip_network('240.0.0.0/4'),
]

BLOCKED_DOMAINS = {
    "localhost",
    "internal",
    "metadata.google.internal",
    "169.254.169.254"
}

ALLOWED_SCHEMES = {"http", "https"}

class SafetyViolation(Exception):
    pass

def validate_url(url: str) -> bool:
    """
    Validates a URL for safety:
    1. Must be http/https.
    2. Must not resolve to private IP.
    3. Must not be on blocklist.
    """
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in ALLOWED_SCHEMES:
            raise SafetyViolation(f"Scheme not allowed: {parsed.scheme}")

        hostname = parsed.hostname
        if not hostname:
            raise SafetyViolation("No hostname found")

        if hostname.lower() in BLOCKED_DOMAINS:
            raise SafetyViolation("Domain blocked explicitly")

        # DNS Resolution check (prevent DNS rebinding attacks realistically requires more, 
        # but this is v0 defense against obvious internal hits)
        try:
            ip = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip)
            for network in PRIVATE_RANGES:
                if ip_obj in network:
                    raise SafetyViolation(f"Resolves to private IP: {ip}")
        except socket.gaierror:
            # If we can't resolve it, we probably can't fetch it, but let playwright try 
            # (or fail safe? fail safe is better)
            raise SafetyViolation(f"Could not resolve hostname: {hostname}")

        return True

    except Exception as e:
        if isinstance(e, SafetyViolation):
            raise
        raise SafetyViolation(f"URL parsing failed: {str(e)}")
