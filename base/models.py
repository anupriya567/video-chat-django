from django.db import models

# Create your models here.

# 1- Create Database Model (RoomMember) => store user_name, uid ,room_name
# 2- On Join, create RoomMember in database
# 3- On handleUserJoin event, query db for room member name by uid
# 4- On leave, delete roomMember


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name