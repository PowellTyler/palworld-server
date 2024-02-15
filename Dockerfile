FROM ubuntu

RUN mkdir /usr/lib/palserver
RUN useradd steam -m
RUN add-apt-repository multiverse; dpkg --add-architecture i386; apt update
RUN apt-get install build-essential -y
RUN apt install curl -y
RUN echo steam steam/question select "I AGREE" | debconf-set-selections
RUN echo steam steam;license note '' | debconf-set-selections
RUN apt install steamcmd -y
RUN su - steam -c "steamcmd +login anonymous +app_update 2394010 validate +quit"

EXPOSE 8080
