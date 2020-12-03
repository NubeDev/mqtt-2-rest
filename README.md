# mqtt-2-rest


### Running on Production

#### One time setup:
- Clone [this](https://github.com/NubeIO/common-py-libs)
- Create `venv` on inside that directory (follow instruction on [here](https://github.com/NubeIO/common-py-libs#how-to-create))

#### Commands:
```bash
sudo bash script.bash start -u=<pi|debian> -dir=<s-mon_dir> -lib_dir=<common-py-libs-dir>
sudo bash script.bash start -u=pi -dir=/home/pi/mqtt-2-rest -lib_dir=/home/pi/common-py-libs
sudo bash script.bash -h
```


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


# MQTT to REST System D


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


##  Settings config
```
cp $PWD/settings/config.example.ini  $PWD/settings/config.ini
nano settings/config.ini

```




# MQTT to REST System D


```
sudo cp systemd/nubeio-mqtt-2-pg.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl disable nubeio-mqtt-2-pg.service
sudo systemctl enable nubeio-mqtt-2-pg.service
sudo journalctl -f -u nubeio-mqtt-2-pg.service
sudo systemctl status nubeio-mqtt-2-pg.service
sudo systemctl start nubeio-mqtt-2-pg.service
sudo systemctl stop nubeio-mqtt-2-pg.service
sudo systemctl restart nubeio-mqtt-2-pg.service

```


##  Settings config
```
cp $PWD/settings/config.example.ini  $PWD/settings/config.ini
nano settings/config.ini

```
