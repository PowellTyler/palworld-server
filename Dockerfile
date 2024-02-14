FROM ubuntu

RUN sudo useradd steam steam
RUN sudo add-apt-repository multiverse; sudo dpkg --add-architecture i386; sudo apt update
RUN sudo apt install steamcmd
RUN sudo su - steam -s steamcmd +login anonymous +app_update 2394010 validate +quit

EXPOSE 8080
