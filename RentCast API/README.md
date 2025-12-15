# Predicting Days on Market for Properties in IL
# api_property_data.py
## Environment
The environment required to run this code is an IDE that supports Python. VSCode and Python 3.13.5 was used when running this file.
## Data
We access the ["sales listings endpoint on RentCast."](https://developers.rentcast.io/reference/sale-listings) through our code. "inactive_listings.csv" is created from running the code and it stores the retrieved data as a csv file.
## API Keys
The code requires you to add your API key into the list of API keys. An API Key ["can be created here."] (https://app.rentcast.io/app/api) by creating an account, API Key, and finally activating the key. Note, it is likely that you will need more than the free 50 requests per key to obtain the same amount of data as us (about 50K rows). 
## Environment
The environment required to run this code is Google Workspace, specifically Google Drive and Google Colab. The necessary files to run the code (such as data files) should be stored in Google Drive and the code will be ran via Google Colab. Google Colab was choosen as the coding environment due to its GPU offerings, which our group did not have on our local machines. It is preferable to use Google Colab Pro so the GPU is consistently available while running the code and the large amount of data can be processed at a reasonable speed.
## Required Packages
The code uses the packages listed below. If the following packages are not already installed, you can use
```
pip install *package name*
```
- requests
- pandas
- os 
## How to Run
1. Open the code in your IDE, preferably VSCode, as that was tested by us.
2. Ensure Python 3.13.5 is enabled and install any packages you are missing.
3. Replace the API keys with your API keys.
4. Run the code and confirm "inactive_listings.csv" was created.
5. Please store "inactive_listings.csv" in your Google Drive, as it must be accessible to our ipynb notebook in Google Colab, which includes our data cleaning, preprocessing, and model code. 
