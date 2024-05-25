import requests
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from flask import Flask, render_template
from geopy.geocoders import Nominatim

# Read the CSV file into a DataFrame
data = pd.read_csv("result.csv")

# Geocode the zip codes using GeoPy

geolocator = Nominatim(user_agent="SolarZipCoder")

print(data.columns)

data = data[data["Zip"].notnull()]

data = data[data["Region"].notnull()]
print(data['Region'].unique())

print(len(data))

data["location"] = data["Zip"].apply(geolocator.geocode)

# Extract the latitude and longitude from the location column
data["latitude"] = data["location"].apply(lambda loc: loc.latitude if loc else None)
data["longitude"] = data["location"].apply(lambda loc: loc.longitude if loc else None)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data["longitude"], data["latitude"]))
gdf.crs = "EPSG:4326"

# Plot the GeoDataFrame
gdf.plot()
plt.show()

# create an interactive map

# filter out NaN latitudes and longitudes
data = data[data["latitude"].notnull()]
data = data[data["longitude"].notnull()]

# filter out lat and long outside of US
data = data[(data["latitude"] > 24) & (data["latitude"] < 50)]

print(data["Sector"].unique())
print(data.columns)

# Create column for map popup that includes company name with website as hyperlink and sector with line breaks
data["popup"] = data["Company Name"] + "<br>" + data["Sector"] + "<br>" + data["Website"]

# Create a map centered at the mean latitude and longitude
m = folium.Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=4)

# Add markers for each zip code, with color based on the sector
for row in data.itertuples():
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=row.popup,
        icon=folium.Icon(color="green" if row.Sector == "Solar" else "blue"),
    ).add_to(m)

# Display the map
m.save("map.html")

# Add map to flask app

app = Flask(__name__)

@app.route("/")

def home():
    return render_template("map.html")

if __name__ == "__main__":
    app.run()

# run the flask app
# python app.py
# open browser and go to http://
# localhost:5000
# to view the map




