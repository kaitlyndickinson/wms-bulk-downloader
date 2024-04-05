import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

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

df = pd.DataFrame(maps_info, columns=["Map Name", "Map URL"])

st.write("## Map Data")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("Map URL")
    for index, row in df.iterrows():
        st.write(row["Map URL"])

with col2:
    st.write("Map Name")
    for index, row in df.iterrows():
        st.write(row["Map Name"])

with col3:
    st.write("Transform Data")
    for index, row in df.iterrows():
        # TODO: this becomes impossible to tell which button aligns with which map
        # look into solutions for this, maybe have to change the format we display in
        
        if st.button(f"Get Data", key=index):
            # TODO: Instead of writing, save data to session state
            # Go to another page with transform form (or maybe a popup, if possible?)
            st.write(f"Got data from {row['Map Name']} and URL: {row['Map URL']}")
