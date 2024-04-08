## _DISCLAIMER_ 
This project is developed for educational purposes as part of a university assignment and is not intended for any unauthorized or malicious use. Any use of this project outside its intended educational scope is the sole responsibility of the user.
## OVERVIEW

The framework is constructed on Django, a sophisticated Python web framework renowned for its emphasis on swift development and orderly, pragmatic design principles. For handling communications, Django Channels and Redis are employed. Both are invaluable tools for managing asynchronous and real-time communications effectively.

PostgreSQL serves as the database backend, offering elevated levels of data management, superior performance, and the capability to handle large volumes of data seamlessly.

The entire system is containerized using Docker, which facilitates effortless deployment, scalability, and the handling of microservices. Additionally, a user interface accessible via a web browser is provided within a container. This interface simulates the behavior of a malevolent user device, allowing for comprehensive testing and evaluation of the system's robustness and security measures.



## SETUP <br>
Open the terminal and write:<br>
`docker-compose up --build`                                 --> build images for each container and start the containers, this will be your main command to activate the environment <br>
<br><br> __Run These Only Once:__ <br>
`docker exec -d server python3 manage.py migrate`           --> run structural migration on the database based on webapp/library/migrations/0001_initial.py migration file<br>
`docker exec -d server python3 manage.py createsuperuser`   --> create server admin and insert your data <br>
## ACCESSING C2 SERVER FROM USER CONTAINER
After activating the environment, open a browser tab and visit: http://localhost:26901/vnc.html?password=headless<br>
You will be redirected to a noVNC page. After connecting, open Firefox inside this new environment, and visit http://server:8000. <br>
You will now see the home page of the C2 Server.  <br>
From here u can login using your admin credentials you set during the SETUP, or access to Django admin management site on http://server:8000/admin, login with your admin credentials and create a new non-admin user. <br>

After authenticating you will be able to see all the devices which are connected to the server, or trying to, and their username and private IPs. <br> 
By clicking on the "Access shell button" you will be able to communicate with one of them. Type "help" for some custom commands (I'm working through some of them) <br>


## NOTES
- You can manually add agent to the environment. Access the docker-compose.yaml file and add new agents, similarly to the already existing one
- __Since im working on a way to manage sudo password on agents, some commands might not be fully working!!!<br>__
Hence, use this `echo 'password' | sudo -S` __`command`__ to send a command with high privileges.<br>
- The only way to actually "eliminate" an agent is by inputting "selfdestroy" command  <br>
- The automatic scroll of the chat is a mistery: it worked previously, now it doesnt. Working on it.

