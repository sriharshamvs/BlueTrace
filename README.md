# BlueTrace

Sets up a Websocket server at 8989, listens to instructins from bluecoat (Broadcast Manager), and starts/stops streams at command.

# Prerequisites 

* Install latest FFMPEG
* Get the latest google-chrome and chromedriver
* Install reqs from py_requirements.txt

```bash
$ apt install python3-dev
$ python3 -m pip install setuptools
$ python3 -m pip install wheel
$ python3 -m pip install -r py_requirements.txt
```

# Running
```bash
$ python3 ws-server.py
```
