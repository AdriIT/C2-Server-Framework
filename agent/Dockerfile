FROM python:3.9

USER root

RUN apt update
#RUN apt-get install iputils-ping -y
#RUN apt install -y python-pip
RUN mkdir /.agent 
# Copy the pwd inside /agent on the container
COPY . /.agent
RUN rm /.agent/Dockerfile

WORKDIR /

# Install Agent dependancies on the container
RUN pip install websocket-client
RUN pip install psutil

#try for x11
# Install X11 server and other necessary dependencies

#RUN apt-get install -y xorg xserver-xorg-video-dummy && \
#    rm -rf /var/lib/apt/lists/*
#
## Configure X11 server to listen only on localhost

#RUN sed -i 's/^\(.*\)Xserver\(.*\)$/\1Xserver -listen tcp -auth $HOME\/.Xauthority -nolisten tcp\2/' /etc/X11/Xwrapper.config

## Set environment variable to disable access control for X11 server

#ENV XAUTHORITY /root/.Xauthority
#
## Copy and set permissions for Xauthority file
#COPY .Xauthority /root/
###



# Start script
#CMD [""]
CMD ["python", ".agent/agent.py"]

