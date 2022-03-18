import streamlit as st
import folium
import osmnx
import networkx as nx
import leafmap.foliumap as leafmap

from typing import Tuple, List
from networkx.classes.multidigraph import MultiDiGraph

# TODO:
#   Cleanup button

BASEMAPS = ['Satellite', 'Roadmap', 'Terrain', 'Hybrid', 'OpenStreetMap']
TRAVEL_MODE = ['Drive', 'Walk', 'Bike']
TRAVEL_OPTIMIZER = ['Length', 'Time']

ADDRESS_DEFAULT = "Grand Place, Bruxelles"

def get_location_from_address(address: str) -> (float, float):
    """ 
    Get (lat, long) coordintates from address
    Args:
        address: string with address
    Returns:
        location: (lat, long) coordinates
    Example:
        location_orig = get_location_from_address("Gare du Midi, Bruxelles")
    """
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent = "myapp")
    location = locator.geocode(address)

    return location.latitude, location.longitude

def get_graph(address_orig: str, address_dest: str) -> (MultiDiGraph, Tuple[float], Tuple[float]):
    """ 
    Convert the origin and destination addresses into (lat, long) coordinates and find the 
    graph of streets from the bounding box.
    Args:
        address_orig: departure address
        address_dest: arrival address
    Returns:
        graph: street graph from OpenStreetMap
        location_orig: departure coordinates
        location_dest: arrival coordinates
    Example:
        graph, location_orig, location_dest = get_graph("Gare du Midi, Bruxelles", "Gare du Nord, Bruxelles")
    """

    MARGIN = 0.1

    # find location by address
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    north = max(location_orig[0],location_dest[0]) + MARGIN
    south = min(location_orig[0],location_dest[0]) - MARGIN
    west = max(location_orig[1],location_dest[1]) + MARGIN
    east = min(location_orig[1],location_dest[1]) - MARGIN

    print(f'North: {north}, South: {south}')
    print(f'West: {west}, East: {east}')

    graph = osmnx.graph.graph_from_bbox(north, south, east, west, network_type='drive', clean_periphery=False)

    return graph, location_orig, location_dest


def find_shortest_path(graph: MultiDiGraph, location_orig: Tuple[float], location_dest: Tuple[float], optimizer: str) -> List[int]:
    """
    Find the shortest path between two points from the street graph
    Args:
        graph: street graph from OpenStreetMap
        location_orig: departure coordinates
        location_dest: arrival coordinates
        optimizer: type of optimizer (Length or Time)
    Returns:
        route:
    """

    # find the nearest node to the departure and arrival location
    node_orig = osmnx.get_nearest_node(graph, location_orig)
    node_dest = osmnx.get_nearest_node(graph, location_dest)

    route = nx.shortest_path(graph, node_orig, node_dest, weight=optimizer.lower())
    return route


def clear_text():
    st.session_state["go_from"] = ""
    st.session_state["go_to"] = ""


st.set_page_config(page_title="🚋 Route finder", layout="wide")

# ====== SIDEBAR ======
with st.sidebar:

    st.title("Choose you travel settings")

    st.markdown("A simple app that finds and displays the shortest path between two points on a map.")

    basemap = st.selectbox("Choose basemap", BASEMAPS)
    if basemap in BASEMAPS[:-1]:
        basemap=basemap.upper()

    transport = st.selectbox("Choose transport", TRAVEL_MODE)
    optimizer = st.selectbox("Choose optimizer", TRAVEL_OPTIMIZER)

    address_from = st.text_input("Go from", key="go_from")
    address_to = st.text_input("Go to", key="go_to")
    
    st.button("Clear all address boxes", on_click=clear_text)
    st.write(address_to)

    st.info(
        "This is an open source project and you are very welcome to contribute your "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/maxmarkov/streamlit-navigator/issues) or "
        "[pull requests](https://github.com/maxmarkov/streamlit-navigator/pulls) "
        "to the [source code](https://github.com/maxmarkov/streamlit-navigator). "
    )




# ====== MAIN PAGE ======
lat, lon = get_location_from_address(address=ADDRESS_DEFAULT)

m = leafmap.Map(center=(lat, lon), zoom=16)

m.add_basemap(basemap)

if address_from and address_to:

    # === FIND PATH ===
    graph, location_orig, location_dest = get_graph(address_from, address_to)

    # Search information 
    st.markdown(f'**From**: {address_from}')
    st.markdown(f'**To**: {address_to}')
    st.write(graph)

    # re-center
    leafmap.Map(center=location_orig, zoom=16)

    # find the nearest node to the start location
    m.add_marker(location=list(location_orig), icon=folium.Icon(color='red', icon='suitcase', prefix='fa'))
    m.add_marker(location=list(location_dest), icon=folium.Icon(color='green', icon='street-view', prefix='fa'))

    # find the shortest path
    route = find_shortest_path(graph, location_orig, location_dest, optimizer)

    osmnx.plot_route_folium(graph, route, m)

else:

    m.add_marker(location=(lat, lon), popup=f"lat, lon: {lat}, {lon}", icon=folium.Icon(color='green', icon='eye', prefix='fa'))
    st.write(f"Lat, Lon: {lat}, {lon}")


m.to_streamlit()
