NAME := palserver
PORT := 8211
PYTHON:= python3.10

install:
	mkdir /var/lib/palserver/mount
	install -d /var/log/$(NAME)
	install /var/log/$(NAME)/access.log
	install package/palserver.service /lib/systemd/system/palserver.service

docker-build:
	podman build -t $(NAME) .

docker-run:
	podman run -dit -p $(PORT):$(PORT) -v .:/usr/lib/$(NAME) -v /var/lib/$(NAME)/mount:/home/steam/Steam/steamapps/common/PalServer -v /var/log/$(NAME):/var/log/$(NAME) --name $(NAME) $(NAME)

docker-ssh:
	podman attach $(NAME)

docker-install:
	$(PYTHON) -m pip install -r requirements.txt
	install package/ARRCON /usr/bin/ARRCON
	install -d /etc/palserver/
	install package/config.ini /etc/palserver/config.ini
	chown steam:steam -R /home/steam/Steam
