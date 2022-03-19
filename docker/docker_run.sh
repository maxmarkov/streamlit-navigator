#!/bin/bash
docker run -it --rm --network=host -p 8501:8501 --name=app streetapp
