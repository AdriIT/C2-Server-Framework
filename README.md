##DISCLAIMER##<br>
This project is developed for educational purposes as part of a university assignment and is not intended for any malicious use 
##

ATTENTION: This project is not YET implemented to work on different machines.<br>

SERVER/USER DEPENDANCIES <br>
install virtual environment<br>
activate your virtual environment<br>
`python -m pip install -U 'channels[daphne]'`  --> install channels and daphne server<br>

We will need a docker container so install docker in your environment<br>
`python3 -m pip install channels_redis`  -->  install this to let channels adapt to redis <br>
`docker run --rm -p 6379:6379 redis:7` --> redis backing store<br>
##

AGENT CLIENT DEPENDANCIES<br>
Install these utils on the agent's machine:<br>

`pip install psutil` --> check ram and memory stats for jittering lookup requests<br>
`pip install keyboard` --> keylogger<br>
`pip install websocket-client` --> to handle communication with server<br>


!!! Since im working on a way to set sudo password, some command might not be fully working !!!<br>
Hence, use this `echo 'password' | sudo -S` __`command`__

QUICK START <br>
`docker-compose build` --> build images for each container<br>
`docker-compose up -d` --> start the containers<br>

*execute this only one time as u first start the environment*
`docker exec -d server python3 manage.py makemigrations` --> create migration file based on django models<br>
`docker exec -d server python3 manage.py migrate` --> run migrations on database <br>
`docker exec -d server python3 manage.py createsuperuser` --> insert your admin data


Create you admin running "python manage.py createsuperuser"<br>
You will need to login as administrator inside http://localhost:8000/admin/<br>
Add a user specifying username and password <br>
http://localhost:8000/login --> login using credentials --> select device test 2 (client.py is supposed to work on test2 chatroom, but you can change the code at line 240* to switch chat room) <br>
Run `python3 client.py`<br>
Send commands in chat, use `help` for a list of commands<br>




http://localhost:26901/vnc.html?password=headless