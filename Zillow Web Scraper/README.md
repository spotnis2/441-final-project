# Predicting Days on Market for Properties in IL
# zillow_scraper.py
## Environment
The environment required to run this code is an IDE that supports Python. VSCode and Python 3.13.5 was used when running this file.
## Data
We access the ["Zillow recently sold data in IL."](https://www.zillow.com/il/sold/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A42.59271593527535%2C%22south%22%3A36.87873322092034%2C%22east%22%3A-85.476223796875%2C%22west%22%3A-93.056790203125%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22curatedCollection%22%3Anull%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%7D) through our code. "zillow_homes.csv" is created from running the code and it stores the retrieved data as a csv file.
## Headers
If the current headers do not work:
1. Go to the ["Zillow recently sold in IL page."](https://www.zillow.com/il/sold/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A42.59271593527535%2C%22south%22%3A36.87873322092034%2C%22east%22%3A-85.476223796875%2C%22west%22%3A-93.056790203125%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%2C%22curatedCollection%22%3Anull%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%7D)
2. ![alt text](image.png) Look for something like this in the Network Tab of Chrome Developer Tools.
3. Click on it and go to request headers, and copy it from there.
## Required Packages
The code uses the packages listed below. If the following packages are not already installed, you can use
```
pip install *package name*
```
- os
- requests
- BeautifulSoup
- json
- csv
- random
- time
- datetime 
- traceback
## How to Run
1. Open the code in your IDE, preferably VSCode, as that was tested by us.
2. Ensure Python 3.13.5 is enabled and install any packages you are missing.
3. Replace the API keys with your API keys.
4. Ensure "illinois_places_bounding_boxes_shuffled.csv" is in the same directory as the code. 
5. Run the code and confirm "zillow_homes.csv" was created.
