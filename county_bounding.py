import geopandas as gpd
import requests, zipfile, io
import os

# 1. Download the Illinois “Place” shapefile (2024/2025 vintage)
url = "https://www2.census.gov/geo/tiger/TIGER2024/PLACE/tl_2024_17_place.zip"
# NOTE: adjust year if newer TIGER released
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("il_places_shapefile")

# 2. Load the shapefile with GeoPandas
shp_path = os.path.join("il_places_shapefile", "tl_2024_17_place.shp")
gdf = gpd.read_file(shp_path)

# 3. Filter to only places in Illinois (state FIPS = 17)
#    (should already be only IL if you downloaded the IL file, but just in case)
gdf = gdf[gdf["STATEFP"] == "17"]

# 4. Compute bounding boxes
gdf["minx"] = gdf.bounds.minx
gdf["miny"] = gdf.bounds.miny
gdf["maxx"] = gdf.bounds.maxx
gdf["maxy"] = gdf.bounds.maxy

# 5. Select relevant columns and export to CSV
out = gdf[["NAME", "GEOID", "minx", "miny", "maxx", "maxy"]]
out = out.sort_values("NAME")
out.to_csv("illinois_places_bounding_boxes.csv", index=False)

print("Exported", len(out), "places to illinois_places_bounding_boxes.csv")
