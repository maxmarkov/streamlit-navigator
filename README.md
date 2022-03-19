# Navigation app

Simple application similar to Google Maps which can be used to find directions between two points. The path is then shown on a map.

**List of current functionalities**:

- [x] Show different types of basemap
- [x] Show the shortest path between two selected points
- [x] Docker

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
