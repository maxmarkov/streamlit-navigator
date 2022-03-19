FROM ubuntu:latest

# Install build tools
RUN apt-get update && apt-get install -y \
        python3-dev python3-pip sudo vim

RUN ln -sv /usr/bin/python3 /usr/bin/python

WORKDIR /home
COPY ./ /home/

RUN pip3 install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
