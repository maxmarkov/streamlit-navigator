#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"maxmarkovvision@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
