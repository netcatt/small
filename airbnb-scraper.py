# Imports
import json
import requests

from bs4 import BeautifulSoup
from typing import Optional, Union

from geopy.geocoders import Nominatim

locator = locator = Nominatim(user_agent="airbnbScraper")

# Constants
SEARCH_ENDPOINT = "https://www.airbnb.com/api/v3/ExploreSearch"
HEADERS = {
    'authority': 'www.airbnb.com',
    'accept-language': 'en-US;q=0.8,en;q=0.7',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'device-memory': '8',
    'dpr': '1',
    'viewport-width': '1360',
    'ect': '4g',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'service-worker-navigation-preload': 'true',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document'
}

SEARCH_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "device-memory": "8",
    "dpr": "1",
    "ect": "4g",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "viewport-width": "678",
    "x-airbnb-graphql-platform": "web",
    "x-airbnb-graphql-platform-client": "minimalist-niobe",
    "x-airbnb-supports-airlock-v2": "true",
    "x-csrf-without-token": "1",
    "x-trc-v3-kraken": "1",
}


def get_api_key() -> Optional[str]:
    """
    This functions sends request to airbnb.com and parses html to find api key
    """

    req = requests.get("https://airbnb.com/", headers=HEADERS)
    soup = BeautifulSoup(req.text, "html.parser")

    config = soup.find("script", attrs={
                       "id": "data-state", "data-state": "true", "type": "application/json"})

    json_config = json.loads(config.string)  # type: ignore

    return json_config["bootstrapData"]["layout-init"]["api_config"]["key"]


def find_listings(location: Union[str, tuple], checkin: str, checkout: str, api_key: str) -> list:
    if type(location) == tuple:
        raw_location = locator.reverse(location).raw

        location = (
            f'{raw_location.get("address", {}).get("road")}, '
            f'{raw_location.get("address", {}).get("house_number")}, '
            f'{raw_location.get("address", {}).get("city")}'
        )

        print("Location: ", location)

    SEARCH_HEADERS["x-airbnb-api-key"] = api_key

    items = []
    offset = 0

    while True:
        params = {
            "operationName": "ExploreSearch",
            "locale": "en",
            "currency": "USD",
            "variables": json.dumps({
                "request": {
                    "metadataOnly": False,
                    "version": "1.7.9",
                    "itemsPerGrid": 50,
                    "tabId": "home_tab",
                    "refinementPaths": [
                        "/homes"
                    ],
                    "datePickerType": "calendar",
                    "checkin": checkin,
                    "checkout": checkout,
                    "source": "structured_search_input_header",
                    "searchType": "search_query",
                    "query": location,
                    "cdnCacheSafe": False,
                    "simpleSearchTreatment": "simple_search_only",
                    "treatmentFlags": [
                        "storefronts_april_2021_homepage_desktop_web",
                        "the_greatest_outdoors_hub_web_moweb",
                        "flexible_dates_options_extend_one_three_seven_days",
                        "super_date_flexibility",
                        "search_input_placeholder_phrases"
                    ],
                    "itemsOffset": offset,
                    "screenSize": "large"
                }
            }),
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "13d050d8facb327f6af8b5cb0b78c618b3d36e2a9f1d6f2a04021b84b9c3f053"
                }
            })
        }

        data = requests.get(
            SEARCH_ENDPOINT, headers=SEARCH_HEADERS, params=params
        ).json()['data']['dora']['exploreV3']

        sections = data['sections']
        for section in sections:
            items_list = section.get('items', [])

            items.extend([
                {
                    "name": item["listing"]["name"],
                    "price": item["pricingQuote"]["price"]["total"]["amount"],
                    "url": "https://www.airbnb.pl/rooms/" + item["listing"]["id"],
                    # "metadata": item
                } for item in items_list
                if item.get("listing") is not None
                and item.get("pricingQuote") is not None
            ])

        offset = len(items)

        if data['metadata']['paginationMetadata']['hasNextPage'] is False:
            break

    return items


def main():
    api_key = get_api_key()

    # response = find_listings((-37.81, 144.96), "2021-07-19", "2021-07-21", api_key) # type: ignore

    listings = find_listings("London", "2021-07-19",
                             "2021-07-21", api_key)  # type: ignore

    print(f"Found: {len(listings)} items")

    print(listings[0])


if __name__ == "__main__":
    main()
