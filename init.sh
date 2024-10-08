${PYTHON} -m pip install -r /usr/lib/${APP_NAME}/requirements.txt

install /usr/lib/${APP_NAME}/package/ARRCON /usr/bin/ARRCON
install -d /etc/${APP_NAME}/
mkdir -p /var/lib/${APP_NAME}/server/Pal/Saved/Config/LinuxServer/
touch /var/lib/${APP_NAME}/server/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini

chown steam:steam -R /home/steam/
chown steam:steam -R /var/lib/palserver

${PYTHON} /usr/lib/${APP_NAME}/palserver
