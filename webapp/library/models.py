from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Device(models.Model):#id os ip mac regione
    username = models.CharField(max_length=30, unique=True)
    ip = models.GenericIPAddressField(default="NULL")
    agent_location = models.TextField(default="NULL")
    status = models.BooleanField()

    def __str__(self):
        return self.name


class Message(models.Model):#tipo esito descrizione payload
    COMMAND = "C"
    REPLY = "R"
    TYPE = [
        (COMMAND, "Command"),
        (REPLY, "Reply"),
    ]
    
    payload = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=1, choices=TYPE)

    user = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    device = models.ForeignKey(Device, to_field="username", on_delete=models.CASCADE)

    