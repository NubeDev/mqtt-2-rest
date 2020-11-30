# mqtt-2-rest


# install issue on PI
Had to install this
`sudo apt install libpq5`


```
git clone --depth 1 https://github.com/NubeDev/mqtt-2-rest
cd mqtt-2-rest/
# if required install python3-venv
sudo apt-get install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
```



```
sudo cp systemd/nubeio-mqtt-2-rest.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl disable nubeio-mqtt-2-rest.service
sudo systemctl enable nubeio-mqtt-2-rest.service
sudo journalctl -f -u nubeio-mqtt-2-rest.service
sudo systemctl status nubeio-mqtt-2-rest.service
sudo systemctl start nubeio-mqtt-2-rest.service
sudo systemctl stop nubeio-mqtt-2-rest.service
sudo systemctl restart nubeio-mqtt-2-rest.service

```


# Settings config
```
cp $PWD/settings/config.example.ini  $PWD/settings/config.ini
nano settings/config.ini

```