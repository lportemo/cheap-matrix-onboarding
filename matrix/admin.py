from django.contrib import admin
from . import helpers
from . import models

# Register your models here.
@admin.register(models.ManagedCommunity)
class ManagedCommunityAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "community_id")


@admin.register(models.ManagedRoom)
class ManagedRoomAdmin(admin.ModelAdmin):
    list_display = ("room_id", "name")


@admin.register(models.MatrixUser)
class MatrixUserAdmin(admin.ModelAdmin):
    list_display = ("user", "matrix_user")
    search_fields = ("user", "matrix_user")


@admin.register(models.UserInvitation)
class UserInvitationAdmin(admin.ModelAdmin):
    list_display = ("user", "room")
    list_filter = ("room", "user")
    actions = [helpers.reinvite]


@admin.register(models.CommunityUserInvitation)
class CommunityUserInvitationInvitation(admin.ModelAdmin):
    list_display = ("user", "community")
    list_filter = ("community", "user")
    actions = [helpers.reinvite]
