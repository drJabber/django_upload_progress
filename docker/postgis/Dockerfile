FROM postgres:11.1

USER root


RUN apt update &&\
          apt install -y libxml2-dev libgeos-dev libproj-dev libgdal-dev

RUN apt install -y postgresql-11-postgis-2.5