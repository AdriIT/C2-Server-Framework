##DISCLAIMER##<br>
This project is developed for educational purposes as part of a university assignment and is not intended for any malicious use 
##

The framework is built on Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design. It is containerized using Docker, allowing for easy deployment and scaling across different environments.


##

__!!! Since im working on a way to manage sudo password on agents, some command might not be fully working !!!<br>__
Hence, use this `echo 'password' | sudo -S` __`command`__

__SETUP & QUICK START <br>__
Open terminal and write:
`docker-compose up --build`                                 --> build images for each container and start the containers, this will be your main command to activate the environment <br>
## run these only once ##
`docker exec -d server python3 manage.py makemigrations`    --> create migration file based on django models<br>
`docker exec -d server python3 manage.py migrate`           --> run migrations on database <br>
`docker exec -d server python3 manage.py createsuperuser`   --> create server admin and insert your data <br>
##
Open a browser tab and visit: http://localhost:26901/vnc.html?password=headless and connect <br>
Open Firefox inside of this new environment, and visit http://server:8000. <br>
You will be redirected to the home page of the C2 Server. 
From here u can login using your admin credentials, or access to Django admin management site on http://server:8000/admin, login with your admin credentials and create a new user. <br>

After authenticating you will be see all the devices which are or were connected to the server, and their username and private IP. <br> 
By clicking on the "Access shell button" you will be able to communicate with one of them. Type "help" for some custom commands (I'm working through on them)  <br>
