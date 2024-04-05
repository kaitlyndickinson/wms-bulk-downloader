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

# Extract map names from URLs
maps_info = []
for link in map_links:
    map_url = link.get("href") 
    parsed_url = urlparse(map_url)

    # Get value of the map parameter
    query_params = parse_qs(parsed_url.query)
    map_param = query_params.get("map")
    if map_param:
        map_name = map_param[0].split("/")[-1].split(".")[0] 
        maps_info.append(map_name)

df = pd.DataFrame(maps_info)

st.write("## Map Names")
st.dataframe(df, height=800) 
