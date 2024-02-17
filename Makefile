NAME := palserver
PORT := 8211
PYTHON:= python3.10

install:
	mkdir -p /var/lib/palserver/{config,mount,storage}
	mkdir -p /var/log/$(NAME)
	echo > /var/log/$(NAME)/access.log
	install package/palserver.service /lib/systemd/system/palserver.service
	install package/config.ini /var/lib/palserver/config/
	docker-build

clean:
	rm -rf /var/lib/$(NAME)
	rm -rf /var/log/$(NAME)
	rm /lib/systemd/system/palserver.service
	docker-stop
	podman rmi $(NAME)

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT)/udp -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME):/var/lib/$(NAME) -v /var/log/$(NAME):/var/log/$(NAME) --name $(NAME) $(NAME)

docker-stop:
	podman stop $(NAME)
	podman rm -f $(NAME)

docker-ssh:
	podman attach $(NAME)
