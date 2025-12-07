import requests
from bs4 import BeautifulSoup
import json
import pprint
import csv
import random
import time
from datetime import datetime 
import pandas as pd

class ZillowScraper():
  #https://github.com/johnbalvin/pyzill/blob/main/src/pyzill/search.py
  headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "origin": "https://www.zillow.com",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  }

  homes_list = []
  column_names = [
    'zpid',
    'streetAddress',
    'zipcode',
    'city',
    'state',
    'latitude',
    'longitude',
    'price',
    'dateSold',
    'bathrooms',
    'bedrooms',
    'livingArea',
    'homeType',
    'homeStatus',
    'daysOnZillow',
    'isFeatured',
    'shouldHighlight',
    'zestimate',
    'rentZestimate',
    'listing_sub_type',
    'isUnmappable',
    'isPreforeclosureAuction',
    'homeStatusForHDP',
    'priceForHDP',
    'timeOnZillow',
    'isNonOwnerOccupied',
    'isPremierBuilder',
    'isZillowOwned',
    'currency',
    'country',
    'taxAssessedValue',
    'isShowcaseListing',
    'has_heating',
    'has_cooling',
    'year_built',
    'list_price',
    'sold_price',
    'price_change',
    'list_date',
    'sold_date',
    'time_on_market'
]

  def fetch(self, url, params=None):
    response = requests.get(url, headers=self.headers, params=params)
    print(response)
    return response
  
  def gen_dict_extract(self, key, var):
    if hasattr(var,'items'): 
        for k, v in var.items(): 
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in self.gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.gen_dict_extract(key, d):
                        yield result
  
  def parse(self, response):
    content = BeautifulSoup(response)
    #grab all the json
    result = content.find("script", id="__NEXT_DATA__")
    data = json.loads(result.string)
    #gen_dict_extract is a function that finds all occurences of a key in a nested dictionary.r
    for result in self.gen_dict_extract("homeInfo", data):
      try:
        sleep_time = random.uniform(5,10)
        time.sleep(sleep_time)
        #construct url string
        url_individual_home = f'https://www.zillow.com/homedetails/{result["streetAddress"].replace(" ", "-")}-{result["city"].replace(" ", "-")}-{result["state"]}-{result["zipcode"]}/{result["zpid"]}_zpid/"'
        resp = self.fetch(url_individual_home)
        content = BeautifulSoup(resp.text)
        result_indiv = content.find("script", id="__NEXT_DATA__")
        data_indiv = json.loads(result_indiv.string)
        home = json.loads(data_indiv["props"]["pageProps"]["componentProps"]["gdpClientCache"])
        listing_key = list(home.keys())[0]
        listing_data = home[listing_key]
        #adding heating, cooling, and year built
        has_heating = listing_data["property"]["resoFacts"].get("hasHeating")
        has_cooling = listing_data["property"]["resoFacts"].get("hasCooling")
        year_built = listing_data["property"]["resoFacts"].get("yearBuilt")
        result["has_heating"] = has_heating
        result["has_cooling"] = has_cooling
        result["year_built"] = year_built

        days_on_market = 0
        format = "%Y-%m-%d"

        date_price_list_sold = [(datetime.strptime(item["date"], format), item["price"]) for item in listing_data["property"]["priceHistory"] if item["event"] == "Sold"]
        date_price_list_listed = [(datetime.strptime(item["date"], format), item["price"]) for item in listing_data["property"]["priceHistory"] if item["event"] == "Listed for sale"]

        max_sold_date_and_price = max(date_price_list_sold, key=lambda x: x[0])
        max_listed_date_and_price = max(date_price_list_listed, key=lambda x: x[0])

        time_on_market = (max_sold_date_and_price[0]-max_listed_date_and_price[0]).days

        list_price = max_listed_date_and_price[1]
        sold_price = max_sold_date_and_price[1]

        price_change =  sold_price - list_price

        result["list_price"] = list_price
        result["sold_price"] = sold_price
        result["price_change"] = price_change
        result["list_date"] = max_listed_date_and_price[0]
        result["sold_date"] = max_sold_date_and_price[0]
        result["time_on_market"] = time_on_market

        self.homes_list.append(result)
        print(self.homes_list)
      except Exception as e:
        print("An error occurred:", e)

  def convert_to_csv(self):
     with open('zillow_homes.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(self.column_names)
        csv_writer.writerows([
        [property.get(column, "") for column in self.column_names] 
        for property in self.homes_list
    ])
  
  def run(self):

    min_lon = -91.513 #west

    max_lon = -87.5 #east

    min_lat = 36.970 #south

    max_lat = 42.508 #north

    step_lon = 0.8026
    step_lat = 0.2769
    for a in range(5):
      for b in range(20):
        for i in range(1, 21):
          try:
            url = f'https://www.zillow.com/il/sold/{i}_p/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A{min_lon}%2C%22east%22%3A{min_lon+step_lon}%2C%22south%22%3A{min_lat}%2C%22north%22%3A{min_lat + step_lat}%7D%2C%22mapZoom%22%3A6%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%2290%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22pagination%22%3A%7B%22currentPage%22%3A{i}%7D%7D'
            params = {
              'searchQueryState': f'{{'
                f'"pagination":{{"currentPage":{i}}},'
                f'"isMapVisible":false,'
                f'"mapBounds":{{"west":{min_lon},"east":{min_lon+step_lon},"south":{min_lat},"north":{min_lat+step_lat}}},'
                f'"mapZoom":6,'
                f'"usersSearchTerm":"IL",'
                f'"regionSelection":[{{"regionId":21,"regionType":2}}],'
                f'"filterState":{{'
                    f'"sort":{{"value":"globalrelevanceex"}},'
                    f'"fsba":{{"value":false}},'
                    f'"fsbo":{{"value":false}},'
                    f'"nc":{{"value":false}},'
                    f'"cmsn":{{"value":false}},'
                    f'"auc":{{"value":false}},'
                    f'"fore":{{"value":false}},'
                    f'"rs":{{"value":true}},'
                    f'"land":{{"value":false}},'
                    f'"manu":{{"value":false}},'
                    f'"doz":{{"value":"90"}}'
                f'}},'
                f'"isListVisible":true'
                f'}}'
            }

            res = self.fetch(url, params)
            self.parse(res.text)
          except:
             print("Error encountered fetching entire page.")
        min_lat += step_lat
      min_lon += step_lon
      

if __name__ == '__main__':
  scraper = ZillowScraper()
  scraper.run()
  scraper.convert_to_csv()