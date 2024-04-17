import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree as ET

st.title("WMS Converter")

# Pull out the map links from the URL
url = "https://astrowebmaps.wr.usgs.gov/webmapatlas/Layers/maps.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
map_links = soup.find_all("a")

maps_info = []

# Save map names and map URLs for processing
# TODO: maybe save off planet name (system), layer type, layer, and layer name,
# to display in the header (save off URL but probably not necessary to display it)
for link in map_links:
    map_url = link.get("href")

    parsed_url = urlparse(map_url)

    # Get value of the map parameter
    query_params = parse_qs(parsed_url.query)
    map_param = query_params.get("map")

    if map_param:
        map_name = map_param[0].split("/")[-1].split(".")[0]
        maps_info.append((map_name, map_url))

# TODO: Even though we aren't directly using "Map URL",
# it's probably necessary when we want to get the XML and pass to GDAL.
df = pd.DataFrame(maps_info, columns=["Map Name", "Map URL"])

st.write("## Map Data")

for index, row in df.iterrows():
    # Creating columns inside iteration allows them to properly align.. dont change this :)
    col1, col2 = st.columns(2)

    with col1:
        st.write(row["Map Name"])

    with col2:
        if st.button(f"Get Data", key=index):
            # TODO: Instead of writing, save data to session state
            # Go to another page with transform form (or maybe a popup, if possible?)
            #st.write(f"Got data from {row['Map Name']} and URL: {row['Map URL']}")

            # Get the maps XML content from the URL
            response = requests.get(row['Map URL'])

            # TODO: remove above code, save data to session state to use in another page, perhaps?
            if response.status_code == 200:
                xml_content = response.text
                st.write(xml_content)


