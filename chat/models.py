from django.db import models


class Message(models.Model):
    owner = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room.name} mesage {self.id}'
    class Meta:
        ordering = ["created"]


class Room(models.Model):
    owner = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
