# make calls to the Manheim API here
import requests
import json
from base64 import b64encode

def authorize():
    # For example, if your application's Client ID is 'zq4hmfg72z3zabc4wr72euyu', and the Secret Code is 'A2Qxe4z83X',
    # put them in a string separated by a colon, as in 'zq4hmfg72z3zabc4wr72euyu:A2Qxe4z83X',
    # and then base­64-encode the string to obtain the encoded string to insert after the 'Basic' keyword
    # http://developer.manheim.com/#/authentication

    client_id = ''
    secret_code = ''
    credentials = client_id + ":" + secret_code
    # token_bytes = credentials.encode('utf-8')
    auth_token = b64encode(credentials.encode('utf-8'))

    headers = {
    'authorization': 'Basic ' + auth_token,
    'content-type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://integration1.api.manheim.com/oauth2/token.oauth2', headers=headers, data=data)
    parse = json.loads(response.text)
    access_token = parse['access_token']
    return access_token
    # print(parse['error'])


def add_unit(type, vin, acctNo):
    # type, vin and acctNo are all required for adding a new unit
    # http://developer.manheim.com/#/apis/inventory/units

    access_token = authorize()

    headers = {
        'authorization': authorize()
    }

    #example data
    data = {
        "type": type,
        "vin": vin,
        "contact": {
            "contactName": "John Doe",
            "companyName": "Porsche Finance",
            "phone": "555-555-5555",
            "email": "johndoe@porsche.com",
            "manheimAccountNumber": "1234567"
        },
    }

    response = requests.post("https://integration1.api.manheim.com/units", headers=headers, data=data)
    parse_url = json.loads(response.text)
    return parse_url['Location'] #this location url is used when creating an offering, or updating a unit



def update_unit(location_url):
    # This method REQUIRES the ID of the unit in the URL of the request.
    # The ID may be retrieved from the Location URL. (parse_url from add_unit())
    # ex. https://integration1.api.manheim.com/units/id/222ccff0-60bc-11e6-b072-136a8f36abcd
    # http://developer.manheim.com/#/apis/inventory/units

    access_token = authorize()

    headers = {
         'authorization': access_token
    }

    #example
    data = {
    'odometer': {
        'reading': '100000'
        }
    }

    response = requests.post("%s", headers=headers, data=data) % location_url
    return response


def retrieve_inventory_by_id(location_url):
    # This method REQUIRES the ID of the unit in the URL of the request.
    # The ID may be retrieved from the Location URL. (parse_url from add_unit())
    # ex. https://integration1.api.manheim.com/units/id/222ccff0-60bc-11e6-b072-136a8f36abcd
    # http://developer.manheim.com/#/apis/inventory/units

    access_token = authorize()

    headers = {
        'authorization': access_token
    }

    response = requests.get('%s') % location_url
    parse = json.loads(response)
    # example: retrieving link to info about account
    account = parse['account']
    return response


def get_valuations(vin, subseries, transmission):
    # use the access token from authorize()

    access_token = authorize()

    headers = {
        'Authorization': access_token,
    }

    response = requests.get('https://integration1.api.manheim.com/valuations/vin/%s/%s/%s', headers=headers) % (vin, subseries, transmission)

    parse = json.loads(response.text)
    return parse


def create_ove_offering(listingType, unit_href, floorPrice, facilitating_href, buyNowPrice, startBidPrice, listingStartDate, listingEndDate):
    # http://developer.manheim.com/#/apis/marketplace/offerings#assign-an-offering-to-a-lane

    access_token = authorize()

    headers = {
        'Authorization': access_token,
    }

    # REQUIRED REQUEST PARAMETERS FOR CREATING OVE OFFERING:
    # listingType, unit, unit.href, floorPrice (req when listingType is BID or BOTH), facilitatingLocation,
    # facilitatingLocation.href, buyNowPrice (BID OR BOTH), startBidPrice (BID OR BOTH), listingStartDate, listingEndDate

    data = {
        'listingType': listingType,
        'unit': {
            'href': unit_href  # URL with information to identify a specific unit ex. https://integration1.api.manheim.com/units/id/222ccff0-60bc-11e6-b072-136a8f36abcd
        },
        'floorPrice': floorPrice,
        'facilitatingLocation': {
            "href": facilitating_href
        },
        'buyNowPrice': buyNowPrice,
        'startBidPrice': startBidPrice,
        'listingStartDate': listingStartDate,
        'listingEndDate': listingEndDate
    }

    response = requests.post('https://integration1.api.manheim.com/offerings/ove', headers=headers, data=data)
    parse = json.loads(response.text)
    return parse


def create_in_lane_offering(unit_href, saleLocation_href):
    access_token = authorize()

    headers = {
        'Authorization': access_token,
    }

    data = {
        'unit':{
                'unit.href': unit_href
            },
        'saleLccation': {
                'saleLocation.href': saleLocation_href
            }
    }

    response = requests.post("https://integration1.api.manheim.com/offerings/ove", headers=headers, data=data)
    parse = json.loads(response.text)
    return parse




def retrieve_offering(location_id):
    # This method REQUIRES the ID of the unit in the URL of the request.
    # The ID may be retrieved from the Location URL. (parse_url from add_unit())
    # ex. https://integration1.api.manheim.com/units/id/222ccff0-60bc-11e6-b072-136a8f36abcd
    # http://developer.manheim.com/#/apis/inventory/units

    access_token = authorize()

    headers = {
        'Authorization': access_token,
    }

    response = requests.get("%s", headers=headers) % (location_id)

    parse = json.loads(response.text)
    unit = parse['unit']
    facilitatingLocation = parse['facilitatingLocation']
    buyerAccount = parse['buyerAccount']
    notes = parse['notes']
    sellerInvoice = parse['sellerInvoice']

    return parse



if __name__ == "__main__":
    authorize()
