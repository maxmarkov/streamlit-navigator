# Navigation app

Streamlit-navigator is a simple navigation app based on [streamlit](https://streamlit.io/) to find directions between two points. When you launch the app, a map is displayed centered on the Grand Place in Brussels. Choose the base map you like in the corresponding selection box. Enter the origin and destination addresses in the appropriate fields and choose the route optimizer. The app will then try to find and display the most optimal route on the map. Click on "Clear all address boxes" to restore all fields to their default values.

**List of current functionalities**:

- [x] Show different types of basemap
- [x] Show the shortest path between two selected points
- [x] Docker
- [ ] Get address from a mouse click

**Core libraries**

- [Streamlit](https://streamlit.io/) to build an app. 
- [OSMnx](https://osmnx.readthedocs.io/en/stable/#) to show a map. 
- [NetworkX](https://networkx.org/) to optimize a graph. 

## Example

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
