from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import requests

# Create your models here.
class ManagedRoom(models.Model):
    room_id = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MatrixUser(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    matrix_user = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.user.email

    class Meta:
        indexes = [models.Index(fields=["user"])]


class UserInvitation(models.Model):
    user = models.ForeignKey(MatrixUser, on_delete=models.CASCADE)
    room = models.ForeignKey(ManagedRoom, on_delete=models.CASCADE)

    def emit_invitation(self):
        payload = {
            "type": "m.login.password",
            "user": settings.MATRIX_USERNAME,
            "password": settings.MATRIX_PASSWORD,
        }
        r = requests.post(
            f"https://{settings.MATRIX_HOMESERVER}/_matrix/client/r0/login",
            json=payload,
        )
        access_token = r.json().get("access_token")
        if not access_token:
            return False
        r = requests.post(
            f"https://{settings.MATRIX_HOMESERVER}/_matrix/client/r0/rooms/{self.room.room_id}/invite",
            params={"access_token": access_token},
            json={"user_id": self.user.matrix_user},
        )

    def __str__(self):
        return f"{self.user} in {self.room}"

    class Meta:
        unique_together = [["user", "room"]]
