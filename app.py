import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
from streamlit_folium import st_folium

import leafmap.foliumap as leafmap
import folium

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx

# https://habr.com/en/amp/post/654239/
# TODO:
#   1. Plot a path graph on top of folium map
#   2. Path and request cleanup button
#   3. Code refactoring
#   4. Get coordinates from a click on the map: bidirectional communication between Folium JS and Python 

BASEMAPS = ['OpenStreetMap', 'Roadmap', 'Satellite', 'Terrain', 'Hybrid']
TRAVEL_MODE = ['Walk', 'Drive', 'Bike', 'Walk']
TRAVEL_OPTIMIZER = ['Time', 'Length']

ADDRESS_DEFAULT = "Grand Place"

st.set_page_config(page_title="🚋 Route finder", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:
    st.title("Choose you travel settings")
    basemap = st.selectbox("Choose basemap", BASEMAPS)
    transport = st.selectbox("Choose transport", TRAVEL_MODE)
    optimizer = st.selectbox("Choose optimizer", TRAVEL_OPTIMIZER)

    address = st.text_input("Location")

    address_from = st.text_input("Go from")
    address_to = st.text_input("Go to")

    locator = Nominatim(user_agent = "myapp")

    if not address:
        address = ADDRESS_DEFAULT
    
    location = locator.geocode(address)
    
    location_latlon = [location.latitude, location.longitude]
    
    if basemap in BASEMAPS[1:]:
        basemap=basemap.upper()

    # Define bokeh Button instance
    # https://docs.bokeh.org/en/latest/docs/reference/models/widgets/buttons.html
    loc_button = Button(label="Get Device Location", width_policy = 'auto', margin = (0, 0, 0, 0), height_policy = 'auto')
    loc_button.js_on_event(
        "button_click",
        CustomJS(
            code="""
        navigator.geolocation.getCurrentPosition(
            (loc) => {
                document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
            }
        )
        """
        ),
    )
    
    # streamlit event
    result = streamlit_bokeh_events(
        loc_button,
        events="GET_LOCATION",
        key="get_location",
        refresh_on_update=False,
        override_height=35,
        debounce_time=0,
    )

    if result:
        if "GET_LOCATION" in result:
            loc = result.get("GET_LOCATION")
            location_latlon = [loc.get("lat"), loc.get("lon")]


lat, lon = location_latlon[0], location_latlon[1]
st.write(f"Lat, Lon: {lat}, {lon}")

m = leafmap.Map(center=(lat, lon), zoom=16)
m.add_basemap(basemap)
popup = f"lat, lon: {lat}, {lon}"
m.add_marker(location=(lat, lon), popup=popup)
#m.to_streamlit()
#{'last_clicked': {'lat': 50.79705198089481, 'lng': 4.3369388580322275}, 'last_object_clicked': None, 'all_drawings': None, 'last_active_drawing': None, 'bounds': {'_southWest': {'lat': 50.79162657276397, 'lng': 4.332754611968995}, '_northEast': {'lat': 50.80112062370733, 'lng': 4.343483448028565}}}
mapdata = st_folium(m, height = 800, width = 1800)

if mapdata:
    if mapdata['last_clicked']:
        marker = mapdata['last_clicked']
        #m.add_marker(location=(marker['lat'], marker['lng']))#, popup=popup)

if address_from and address_to:

    location_from = locator.geocode(address_from)
    location_to = locator.geocode(address_to)
    print(f' FROM: {location_from},\n TO: {location_to}')

    graph = ox.graph_from_place(address_from, network_type = transport.lower())

    # find the nearest node to the start location
    orig_node = ox.get_nearest_node(graph, (location_from.latitude, location_from.longitude))
    # find the nearest node to the end location
    dest_node = ox.get_nearest_node(graph, (location_to.latitude, location_to.longitude))

    # find the shortest path
    route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer.lower())

    #node_pairs = zip(route[:-1], route[1:])
    #uvk = ((u, v, min(graph[u][v], key=lambda k: graph[u][v][k]["length"])) for u, v in node_pairs)
    #gdf_edges = ox.utils_graph.graph_to_gdfs(graph.subgraph(route), nodes=False).loc[uvk]

    #print(route)

    shortest_route_map = ox.plot_route_folium(graph, route, m)
