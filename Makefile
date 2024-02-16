NAME := palserver
PORT := 8211

install:
	install package/ARRCON /usr/bin/ARRCON
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/palserver-update.service /lib/systemd/system/palserver-update.service
	install -d /etc/palserver/
	install package/config.ini /etc/palserver/config.ini
	chown steam:steam -R /home/steam/Steam

init:
	mkdir /var/lib/palserver/mount

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT) -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME)/mount:/home/steam/Steam/steamapps/common/PalServer --name $(NAME) $(NAME)
	podman exec $(NAME) /bin/sh -c 'cd /usr/lib/palserver; make install'

docker-ssh:
	podman attach $(NAME)
