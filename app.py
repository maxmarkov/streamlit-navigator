import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap

# TODO:
#   Graph from bbox
#   Cleanup button

BASEMAPS = ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap']
TRAVEL_MODE = ['Drive', 'Walk', 'Bike']
TRAVEL_OPTIMIZER = ['Length', 'Time']

ADDRESS_DEFAULT = "Grand Place, Bruxelles"

def get_location_from_address(address: str) -> (float, float):
    """ """
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent = "myapp")
    location = locator.geocode(address)

    return location.latitude, location.longitude

def get_graph(address1, address2):
    """ """
    location1 = get_location_from_address(address1)
    location2 = get_location_from_address(address2)

    north = max(location1[0],location2[0])
    south = min(location1[0],location2[0])
    west = max(location1[1],location2[1])
    east = min(location1[1],location2[1])
    print(f'NS {north}, {south}')
    print(f'WE {west}, {east}')
    graph = osmnx.graph.graph_from_bbox(north, south, east, west, network_type='drive', clean_periphery=True)

    return graph


st.set_page_config(page_title="🚋 Route finder", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:

    st.title("Choose you travel settings")

    st.markdown("A simple app that finds and displays the shortest path between two points on a map.")

    basemap = st.selectbox("Choose basemap", BASEMAPS)
    transport = st.selectbox("Choose transport", TRAVEL_MODE)
    optimizer = st.selectbox("Choose optimizer", TRAVEL_OPTIMIZER)

    address_from = st.text_input("Go from")
    address_to = st.text_input("Go to")

    if basemap in BASEMAPS[:-1]:
        basemap=basemap.upper()

    st.info(
        "This is an open source project and you are very welcome to contribute your "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/maxmarkov/streamlit-navigator/issues) or "
        "[pull requests](https://github.com/maxmarkov/streamlit-navigator/pulls) "
        "to the [source code](https://github.com/maxmarkov/streamlit-navigator). "
    )




# ====== MAIN PAGE ======
lat, lon = get_location_from_address(address=ADDRESS_DEFAULT)
st.write(f"Lat, Lon: {lat}, {lon}")

m = leafmap.Map(center=(lat, lon), zoom=16)
m.add_marker(location=(lat, lon), popup=f"lat, lon: {lat}, {lon}", icon=folium.Icon(color='green', icon='eye', prefix='fa'))

m.add_basemap(basemap)

# === FIND PATH === 
if address_from and address_to:

    graph = get_graph(address_from, address_to)

    ## find the nearest node to the start location
    #orig_node = ox.get_nearest_node(graph, (location_from.latitude, location_from.longitude))
    #m.add_marker(location=[location_from.latitude, location_from.longitude], icon=folium.Icon(color='lightgray', icon='home', prefix='fa'))

    ## find the nearest node to the end location
    #dest_node = ox.get_nearest_node(graph, (location_to.latitude, location_to.longitude))
    #m.add_marker(location=[location_to.latitude, location_to.longitude], Color='Green')

    ## find the shortest path
    #route = nx.shortest_path(graph, orig_node, dest_node, weight=optimizer.lower())

    ##plot_route_folium(graph, route, m)
    #shortest_route_map = ox.plot_route_folium(graph, route, m)

m.to_streamlit()
