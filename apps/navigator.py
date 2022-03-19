import osmnx
import networkx as nx

from typing import Tuple, List
from networkx.classes.multidigraph import MultiDiGraph

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


def get_graph_from_mode(address_orig: str, address_dest: str, mode: str, city: str="Brussels", dist: float=1000.) -> (MultiDiGraph, Tuple[float], Tuple[float]):
    """
    Convert the origin and destination addresses into (lat, long) coordinates and find the
    graph of streets from the bounding box.
    Args:
        address_orig: departure address
        address_dest: arrival address
        mode: get graph from place or from address
        city: name of the city/town
        dist: distance from the original address in meters
    Returns:
        graph: street graph from OpenStreetMap
        location_orig: departure coordinates
        location_dest: arrival coordinates
    Examples:
        graph, location_orig, location_dest = get_graph_from_mode("Gare du Midi, Bruxelles", "Gare du Nord, Bruxelles", mode="place", city="Bruxelles")
        graph, location_orig, location_dest = get_graph_from_mode("Gare du Midi, Bruxelles", "Gare du Nord, Bruxelles", mode="address", dist=2000)
    """

    assert mode in ['place', 'address']

    # find location by address
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    if mode == 'place':
        graph = osmnx.graph_from_place(city, network_type = 'drive')
    else:
        graph = osmnx.graph.graph_from_address(address_orig, dist=dist, dist_type='bbox', network_type = 'drive')

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
