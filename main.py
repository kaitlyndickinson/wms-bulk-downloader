import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# Pull out the map links from the URL
url = "https://astrowebmaps.wr.usgs.gov/webmapatlas/Layers/maps.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
map_links = soup.find_all("a")

maps_info = []
selected_maps = []
max_height = 300
download_folder = "downloaded_maps"

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

st.title("WMS Downloader")

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
    with st.status("Downloading data..."):
        for map_url in selected_maps:
            response = requests.get(map_url)

            if response.status_code == 200:
                xml_content = response.text

                # Save XML content to a file
                # TODO: this will most likely fail on the duplicate file names,
                # should check if it exists first than use a random id or something
                file_name = f"{map_url.split('/')[-1].split('.')[0]}.xml"
                file_path = os.path.join(download_folder, file_name)

                try:
                    with open(file_path, "w") as f:
                        f.write(xml_content)
                    st.write(f"Successfully downloaded: {file_name}")
                except Exception as e:
                    st.error(f"Error downloading: {file_name}: {e}")
