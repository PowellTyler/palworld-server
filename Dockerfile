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
RUN apt install steamcmd -y
RUN mkdir -p /home/steam/.steam/sdk64/
RUN /usr/games/steamcmd +login anonymous +app_update 1007 +quit
RUN cp ~/Steam/steamapps/common/Steamworks\ SDK\ Redist/linux64/steamclient.so /home/steam/.steam/sdk64/

# Server
EXPOSE 8211/udp
# RCON
EXPOSE 25575/tcp
