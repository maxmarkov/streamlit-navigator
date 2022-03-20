# Navigation app

Streamlit-navigator is a simple navigation app based on [streamlit](https://streamlit.io/) to find directions between two points. When you launch the app, a map is displayed centered on the Grand Place in Brussels. Choose the base map you like in the corresponding selection box. Enter the origin and destination addresses in the appropriate fields and choose the route optimizer. The app will then try to find and display the most optimal route on the map. Click on "Clear all address boxes" to restore all fields to their default values.

**List of current functionalities**:

- [x] Show different types of basemap
- [x] Show the shortest path between two selected points
- [x] Docker
- [ ] Get address from a mouse click

Find the route between Battery Park and Times Square in New York City.

![show different maps](demo/demo_navigator.gif)

## Docker

Build a docker container
```
./docker/docker_build.sh
```

Launch the docker container
```
./docker/docker_run.sh
```

Copy network URL into you browser

## Local 
Install all requirements
```
pip install -r requirements.txt
```
Launch the app
```
streamlit run app.py
```

Copy network URL into you browser

## Note on graph construction

To find the optimal route, it is necessary to build a graph consisting of roads and intersections. The default way to do it is to build a bounding box from the coordinates of the source and destination addresses (we add some margin) provided by the user. This is done by using the `graph_from_bbox` function from OSMnx. However, according to my tests, the method is not the fastest and takes a really long time for even relatively small distances. A faster way to construct a graph is to use the `graph_from_place` and `graph_from_address` functions. For the former one, I recommend to provide the city/town name (a hardcoded variable). For the latter one, you need to specify the distance from origin in meters (also a hardcoded variable). You can change it by uncommenting the lines of code below "FIND THE PATH" in `app.py`.

## Core libraries

- [Streamlit](https://streamlit.io/) to build an app. 
- [OSMnx](https://osmnx.readthedocs.io/en/stable/#) to show a map. 
- [NetworkX](https://networkx.org/) to optimize a graph. 
