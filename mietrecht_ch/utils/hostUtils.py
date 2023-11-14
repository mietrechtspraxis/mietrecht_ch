
from urllib.parse import urlparse
import frappe


def get_website_url():
    site_url = frappe.local.request.url

    parsed_url = urlparse(site_url)

    # Extract the host
    host = parsed_url.netloc
    if parsed_url.scheme:
        host = parsed_url.scheme + '://' + host

    return host