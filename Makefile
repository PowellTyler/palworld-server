NAME := palserver
PORT := 8211
PYTHON:= python3.10

install:
	mkdir -p /var/lib/palserver/mount/config
	mkdir -p /var/lib/palserver/mount/server
	mkdir -p /var/lib/palserver/mount/storage
	mkdir -p /var/lib/palserver/mount/backup
	mkdir -p /var/log/$(NAME)
	mkdir -p /usr/lib/palserver
	cp -r palserver/ package/ init.sh requirements.txt /usr/lib/palserver/
	touch /var/log/$(NAME)/access.log
	install package/palserver.service /lib/systemd/system/palserver.service
	touch /var/lib/palserver/mount/config/config.cfg
	podman build -t $(NAME) .

clean: docker-stop
	rm -rf /var/lib/$(NAME)
	rm -rf /var/log/$(NAME)
	rm -rf /usr/lib/$(NAME)
	rm -f /lib/systemd/system/palserver.service
	podman rmi $(NAME)

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT)/udp -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME)/mount:/var/lib/$(NAME) -v /var/log/$(NAME):/var/log/$(NAME) --name $(NAME) $(NAME)

docker-stop:
	podman stop --ignore $(NAME)
	podman rm -f --ignore $(NAME)

docker-ssh:
	podman attach $(NAME)
