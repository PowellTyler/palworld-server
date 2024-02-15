NAME := palserver
PORT := 8081

install:
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/palserver-update.service /lib/systemd/system/palserver-update.service
	install -d /etc/palserver/
	install palserver_updater/config/config.ini /etc/palserver/config.ini

init:
	mkdir /var/lib/palserver

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT) -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME):/home/steam/Steam/steamapps/common/PalServer/Pal/Saved --name $(NAME) $(NAME)
	podman exec $(NAME) /bin/sh -c 'cd /usr/lib/palserver; make install'

docker-ssh:
	podman attach $(NAME)