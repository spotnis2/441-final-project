import requests
import pandas as pd
import os
import csv

#sonika's api key - 6dd6261388c448bdb6917c07705db29e
#kinjal's api key - 114e4969fc744714a9d676259631ff04
#peter's api key - 8229c7243a97433285bc8d44b037fad7
#sonika api key 2 - 113586579daf40debf95e1e114ba331d


api_keys = ['6dd6261388c448bdb6917c07705db29e', 
            '114e4969fc744714a9d676259631ff04', 
            '8229c7243a97433285bc8d44b037fad7',
            '113586579daf40debf95e1e114ba331d'
            ]
current_api_key_ind = 0
current_requests_per_key = 0

headers = {
    "accept": "application/json",
    "X-Api-Key": api_keys[current_api_key_ind]
}

# column_names_recently_sold_properties = [
#     "id",
#     "addressLine1",
#     "addressLine2",
#     "city",
#     "state",
#     "zipCode",
#     "county",
#     "latitude",
#     "longitude",
#     "propertyType",
#     "bedrooms",
#     "bathrooms",
#     "squareFootage",
#     "lotSize",
#     "yearBuilt",
#     "lastSaleDate",
#     "lastSalePrice",
#     "features.architectureType",
#     "features.cooling"
#     "features.coolingType",
#     "features.exteriorType",
#     "features.fireplace",
#     "features.fireplaceType",
#     "features.floorCount",
#     "features.foundationType",
#     "features.garage",
#     "features.garageSpaces",
#     "features.garageType",
#     "features.heating",
#     "features.heatingType",
#     "features.pool",
#     "features.poolType",
#     "features.roofType",
#     "features.roomCount",
#     "features.unitCount",
#     "features.viewType",
#     "property_tax_ratio",
#     "historical_sales",  
# ]

column_names_inactive_listings = [
    "id",
    "formattedAddress",
    "addressLine1",
    "addressLine2",
    "city",
    "state",
    "stateFips",
    "zipCode",
    "county",
    "countyFips",
    "latitude",
    "longitude",
    "propertyType",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "lotSize",
    "yearBuilt",
    "hoa.fee",
    "status",
    "price",
    "listingType",
    "listedDate",
    "removedDate",
    "createdDate",
    "lastSeenDate",
    "daysOnMarket",
    "listingOffice.name",
    "listingOffice.phone",  
]

def make_csv(df, file_name):
    file_created = os.path.isfile(file_name)
    
    if not file_created:
        df.to_csv(file_name, 
                  index=False)
    else:
        df.to_csv(file_name, 
                  mode='a',
                  header=False,
                  index=False)

# def get_properties_data():
#     # Calls properties API
#     properties_limit = 500
#     properties_offset = 0 
    
#     global current_requests_per_key, current_api_key_ind, headers

#     while True:
#         url = f"https://api.rentcast.io/v1/properties?state=IL&saleDateRange=90&limit={properties_limit}&offset={properties_offset}&includeTotalCount=true"
        
#         # check available keys and number of requests to determine which key to use
#         if current_requests_per_key >= 1:
#             current_api_key_ind += 1
#             if current_api_key_ind >= len(api_keys):
#                 print("OUT OF KEYS")
#                 break
#             else:
#                 headers["X-Api-Key"] = api_keys[current_api_key_ind]
#                 current_requests_per_key = 0

#         response = requests.get(url, headers=headers)

#         print("PROPERTIES")
#         print(response.headers)
        
#         current_requests_per_key += 1

#         response_as_json = response.json() #list of dicts

#         if response_as_json == []:
#             break

#         for item in response_as_json:
#             # tax ratio computation initialization
#             property_tax_ratio = None

#             # tax assessment value
#             if ("taxAssessments" not in item.keys()) or ("propertyTaxes" not in item.keys()) or ("history" not in item.keys()):
#                 continue
            
#             tax_assessment_years = [int(year) for year in item["taxAssessments"].keys()]
#             most_recent_tax_assessment_year = max(tax_assessment_years)
#             tax_assessment_value = item["taxAssessments"][str(most_recent_tax_assessment_year)]["value"]

#             # property taxes total
#             property_taxes_years = [int(year) for year in item["propertyTaxes"].keys()]
#             most_recent_property_taxes_year = max(property_taxes_years)
#             property_taxes_total = item["propertyTaxes"][str(most_recent_property_taxes_year)]["total"]

#             # tax ratio computation
#             if most_recent_tax_assessment_year == most_recent_property_taxes_year:
#                 property_tax_ratio = int(property_taxes_total) / int(tax_assessment_value)
            
#             #add key to dictionary
#             item["property_tax_ratio"] = property_tax_ratio
            
#             # count of historical sales
#             history_len = len(item["history"])
#             item["historical_sales"] = history_len   

#         flattened_json = pd.json_normalize(response_as_json)

#         # set None for column values that are not in the flattened json
#         for column_name in column_names_recently_sold_properties:
#             if column_name not in flattened_json.columns:
#                 flattened_json[column_name] = None

#         recently_sold_properties_df = flattened_json[column_names_recently_sold_properties]
        
#         make_csv(recently_sold_properties_df, "recently_sold_properties.csv")

#         properties_offset += properties_limit

def get_listings_data():
    # Calls listings API
    listings_limit = 500
    listings_offset = 0 
    
    global current_requests_per_key, current_api_key_ind, headers

    while True:
        url = f"https://api.rentcast.io/v1/listings/sale?state=IL&status=Inactive&limit={listings_limit}&offset={listings_offset}"
        
        # check available keys and number of requests to determine which key to use
        if current_requests_per_key > 25:
            current_api_key_ind += 1
            if current_api_key_ind >= len(api_keys):
                print("OUT OF KEYS")
                break
            else:
                headers["X-Api-Key"] = api_keys[current_api_key_ind]
                current_requests_per_key = 0

        response = requests.get(url, headers=headers)

        current_requests_per_key += 1

        response_as_json = response.json()

        if response_as_json == []:
            break
        
        flattened_json = pd.json_normalize(response_as_json)

        # set None for column values that are not in the flattened json
        for column_name in column_names_inactive_listings:
            if column_name not in flattened_json.columns:
                flattened_json[column_name] = None

        inactive_listings_df = flattened_json[column_names_inactive_listings]

        make_csv(inactive_listings_df, "inactive_listings.csv")
            
        listings_offset += listings_limit

if __name__ == '__main__':

    # get_properties_data()
    get_listings_data()
    
    #Merge CSV files
    # recently_sold_properties_df = pd.read_csv("recently_sold_properties.csv")
    inactive_listings_df = pd.read_csv("inactive_listings.csv")

    # final_properties_data_df = pd.merge(recently_sold_properties_df, inactive_listings_df, on="id", how="inner")

    # final_properties_data_df.to_csv("final_properties_data.csv")