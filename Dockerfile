FROM ubuntu

RUN useradd steam -m
RUN add-apt-repository multiverse; dpkg --add-architecture i386; apt update

RUN echo steam steam/question select "I AGREE" | debconf-set-selections
RUN echo steam steam;license note '' | debconf-set-selections
RUN apt install steamcmd -y

EXPOSE 8080
