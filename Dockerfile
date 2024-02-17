FROM ubuntu

RUN mkdir /usr/lib/palserver
RUN useradd steam -m
RUN echo steam > passwd steam
RUN add-apt-repository multiverse; dpkg --add-architecture i386; apt update
RUN apt-get install build-essential -y
RUN apt-get install python3.10 python3-pip -y
RUN apt install curl -y
RUN echo steam steam/question select "I AGREE" | debconf-set-selections
RUN echo steam steam;license note '' | debconf-set-selections
RUN su - steam -c apt install steamcmd -y

# Server
EXPOSE 8211/udp
# RCON
EXPOSE 25575/tcp
