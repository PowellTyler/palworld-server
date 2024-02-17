NAME := palserver
PORT := 8211
PYTHON:= python3.10

install:
	mkdir -p /var/lib/palserver/config
	mkdir -p /var/lib/palserver/mount
	mkdir -p /var/lib/palserver/storage
	mkdir -p /var/log/$(NAME)
	echo > /var/log/$(NAME)/access.log
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/config.ini /var/lib/palserver/config/
	docker-build

clean: docker-stop
	rm -rf /var/lib/$(NAME)
	rm -rf /var/log/$(NAME)
	rm -f /lib/systemd/system/palserver.service
	podman rmi $(NAME)

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT)/udp -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME):/var/lib/$(NAME) -v /var/log/$(NAME):/var/log/$(NAME) --name $(NAME) $(NAME)

docker-stop:
	podman stop --ignore $(NAME)
	podman rm -f --ignore $(NAME)

docker-ssh:
	podman attach $(NAME)
