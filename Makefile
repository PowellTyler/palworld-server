NAME := palserver
PORT := 8081

install:
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/palserver-update.service /lib/systemd/system/palserver-update.service
	install -d palserver_updater/config/config.ini /etc/palserver/config.ini
	cp palserver_updater /usr/shared/pyshared/

init:
	mkdir /var/lib/palserver

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT) -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME):/home/steam/Steam/steamapps/common/PalServer/Pal/Saved --name $(NAME) $(NAME)
	podman exec $(NAME) /bin/sh -c 'cd /var/lib/palserver; make install'

docker-ssh:
	podman attach $(NAME)