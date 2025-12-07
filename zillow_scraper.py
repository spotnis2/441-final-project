import requests
from bs4 import BeautifulSoup
import json
import pprint
import csv
import random
import time
from datetime import datetime 
import pandas as pd
import traceback
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
  
  total_results_for_county = 0
  current_results_for_county = 0
   

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
  
  def parse(self, response, i):
    content = BeautifulSoup(response)
    #grab all the json
    result = content.find("script", id="__NEXT_DATA__")
    data = json.loads(result.string)
    
    if i == 1:
      try:
        gen = self.gen_dict_extract("totalResultCount", data)
        self.total_results_for_county = next(gen)
        print(self.total_results_for_county)
      except Exception as e:
        print("Problem getting total count", e)
    #gen_dict_extract is a function that finds all occurences of a key in a nested dictionary.r
    for result in self.gen_dict_extract("homeInfo", data):
      self.current_results_for_county += 1
      try:
        sleep_time = random.uniform(5,10)
        time.sleep(sleep_time)
        #construct url string
        url_individual_home = f'https://www.zillow.com/homedetails/{result["streetAddress"].replace(" ", "-")}-{result["city"].replace(" ", "-")}-{result["state"]}-{result["zipcode"]}/{result["zpid"]}_zpid/"'
        print(url_individual_home)
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
        print(result)
      except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()

  def convert_to_csv(self):
     with open('zillow_homes.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(self.column_names)
        csv_writer.writerows([
        [property.get(column, "") for column in self.column_names] 
        for property in self.homes_list
    ])
  
  def run(self):
    with open("illinois_places_bounding_boxes.csv", "r") as file:
      for line in file:
        columns = line.strip().split(",")
        if columns[0] == "NAME": #first line
          continue
        print("COLUMNS", columns)
        self.current_results_for_county = 0
            
        for i in range(1, 21):
          try:
            url = f'https://www.zillow.com/{columns[0].lower()}-il/sold/{i}_p/?category=RECENT_SEARCH&searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22currentPage%3A{i}%7D%2CisMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A{columns[2]}%2C%22east%22%3A{columns[4]}%2C%22south%22%3A{columns[3]}%2C%22north%22%3A{columns[5]}%7D%2C%22usersSearchTerm%22%3A%22{columns[0]}%20IL%22%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%2290%22%7D%7D%2C%22isListVisible%22%3Atrue%7D'
            print(url)
            params = {
              'searchQueryState': f'{{'
                f'"pagination":{{"currentPage":{i}}},'
                f'"isMapVisible":false,'
                f'"mapBounds":{{"west":{columns[2]},"east":{columns[4]},"south":{columns[3]},"north":{columns[5]}}},'
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
            self.parse(res.text, i)
          except Exception as e:
              print("Error encountered fetching entire page.", e)
              traceback.print_exc()
          if self.current_results_for_county >= self.total_results_for_county:
               break


      

if __name__ == '__main__':
  scraper = ZillowScraper()
  scraper.run()
  scraper.convert_to_csv()