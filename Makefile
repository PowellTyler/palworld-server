NAME := palserver
PORT := 8211
PYTHON:= python3.10

install:
	mkdir -p /var/lib/palserver/mount
	mkdir -p /var/log/$(NAME)
	echo > /var/log/$(NAME)/access.log
	install package/palserver.service /lib/systemd/system/palserver.service
	docker-build

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT)/udp -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME)/mount:/home/steam/Steam/steamapps/common/PalServer -v /var/log/$(NAME):/var/log/$(NAME) --name $(NAME) $(NAME)

docker-stop:
	podman stop --ignore -t 10 $(NAME)
	podman rm -f --ignore -t 10 $(NAME)

docker-ssh:
	podman attach $(NAME)
