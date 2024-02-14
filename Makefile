NAME := palserver
PORT := 8081

install:
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/palserver-update.service /lib/systemd/system/palserver-update.service
	install -d palserver_updater/config/config.ini /etc/palserver/config.ini
	cp palserver_updater /usr/shared/pyshared/

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT) --network=host --dns 8.8.8.8 --name $(NAME) $(NAME)

docker-ssh:
	podman attach $(NAME)