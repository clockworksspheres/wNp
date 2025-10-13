#!/usr/bin/env -S python -u

import json

from noaa_sdk import NOAA


class forecast():
    def __init__(self):
  
        self.n = NOAA()

    def set_zip(self, pzip):
        self.pzip = pzip

    def set_country(self, country):
        self.country = country

    def get_forecast(self):
        res = self.n.get_forecasts(self.pzip, self.country)
        for item in res:
            # print(json.dumps(item, indent=4))
            print("{")
            print(f"temperature: {item['temperature']}")
            print(f"dewpoint:{item['dewpoint']['value']}")
            print(f"relativeHumidity :{item['relativeHumidity']['value']}")
            # print(f":{}")
            # print(f":{}")
            print("}")

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument("-z", "--zipcode", default="00000", help="zipcode to gather data on")
    parser.add_argument("-c", "--country", default='US', help="country to gather data on")
    args = parser.parse_args()

    if not args.country:
        country = 'US'
    else:
        country = args.country

    future = forecast()
    future.set_zip(args.zipcode)
    future.set_country(country)
    future.get_forecast()


