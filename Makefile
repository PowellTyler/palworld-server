NAME := palserver
PORT := 8081

install:
	install palserver.service /lib/systemd/system/palserver.service
	install palserver-update.service /lib/systemd/system/palserver-update.service

docker-build:
	podman build -t ${NAME} .

docker-run:
	podman run -p $(PORT):$(PORT) --name $(NAME) $(NAME)