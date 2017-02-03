FROM ubuntu:14.04

MAINTAINER Harvey Kim <vaporize93@gmail.com>

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=./possster
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/possster

# Timezone
ENV TZ=Asia/Seoul
RUN echo $TZ | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip nginx libjpeg8-dev 

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir logs
RUN mkdir media

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Install Python dependencies
RUN pip3 install -r $DOCKYARD_SRVHOME/requirements.txt

# Port to expose
EXPOSE 80

# Copy entrypoint script into the image
COPY entry.sh /
WORKDIR $DOCKYARD_SRVPROJ
ENTRYPOINT ["/entry.sh"]




