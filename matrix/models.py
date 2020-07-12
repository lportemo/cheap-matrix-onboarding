from django.db import models
from django.contrib.auth import get_user_model
from . import helpers
import requests
from django.conf import settings

# Create your models here.
class ManagedRoom(models.Model):
    room_id = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ManagedCommunity(models.Model):
    community_id = models.CharField(unique=True, max_length=200)
    friendly_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Managed communities"

    def __str__(self):
        return self.friendly_name


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
    resource_name = "room"

    def emit_invitation(self):
        access_token = helpers.get_access_token()
        r = requests.post(
            f"https://{settings.MATRIX_HOMESERVER}/_matrix/client/r0/rooms/{self.room.room_id}/invite",
            params={"access_token": access_token},
            json={"user_id": self.user.matrix_user},
        )

    def __str__(self):
        return f"{self.user} in {self.room}"

    class Meta:
        unique_together = [["user", "room"]]


class CommunityUserInvitation(models.Model):
    user = models.ForeignKey(MatrixUser, on_delete=models.CASCADE)
    community = models.ForeignKey(ManagedCommunity, on_delete=models.CASCADE)
    resource_name = "community"

    def emit_invitation(self):
        access_token = helpers.get_access_token()
        r = requests.put(
            f"https://{settings.MATRIX_HOMESERVER}/_matrix/client/r0/groups/{self.community.community_id}/admin/users/invite/{self.user.matrix_user}",
            params={"access_token": access_token},
            json={},
        )

    def __str__(self):
        return f"{self.user} in {self.community}"

    class Meta:
        unique_together = [["user", "community"]]
