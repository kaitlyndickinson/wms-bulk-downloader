import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree as ET

st.title("WMS Downloader")

# Pull out the map links from the URL
url = "https://astrowebmaps.wr.usgs.gov/webmapatlas/Layers/maps.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
map_links = soup.find_all("a")

maps_info = []
selected_maps = []
max_height = 300  

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

st.write("## Map Data")

# Display map names in a bounded region that users can select from
with st.container(height=max_height):
    for index, map_info in enumerate(maps_info):
        map_name, map_url = map_info
        selected = st.checkbox(map_name, key=f"{index}_{map_url}")
        if selected:
            selected_maps.append(map_url)

# Download selected map XML files
if st.button("Download Maps"):
    for map_url in selected_maps:
        response = requests.get(map_url)

        if response.status_code == 200:
            xml_content = response.text

            # Save XML content to a file, TODO: not really sure if this works properly yet
            file_name = f"{map_url.split('/')[-1].split('.')[0]}.xml"
            with open(file_name, "w") as f:
                f.write(xml_content)
            st.write(f"Downloaded: {file_name}")