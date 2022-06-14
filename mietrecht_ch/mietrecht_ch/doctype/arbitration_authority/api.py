import frappe
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import requests
import json

api_url= 'https://mp-test.libracore.ch'
token= 'b41ffa6b-c188-4ca1-aaf9-06f3081718e9'


@frappe.whitelist(allow_guest=True)
def proxy(plz_city = None):
    if (plz_city == None):
        raise BadRequestException("Please provide the parameter plz_city")

    full_url= '''{apiUrl}/api/method/mietrechtspraxis.api.get_sb?token={token}&plz_city={plz_city}'''.format(apiUrl=api_url, token=token, plz_city=plz_city)
    print(full_url)
    request = requests.get(full_url, verify=False)
    result = json.loads(request.text)
    return result['message']
