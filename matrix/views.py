from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.urls import reverse_lazy

# Create your views here.
class UserCreationView(LoginRequiredMixin, CreateView):
    model = models.MatrixUser
    fields = ["matrix_user"]
    template_name = "matrix/matrix-user.html"
    success_url = reverse_lazy("matrix:join")

    def dispatch(self, request, *args, **kwargs):
        if models.MatrixUser.objects.filter(user=self.request.user).exists():
            return redirect("matrix:join")
        return super(UserCreationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserCreationView, self).form_valid(form)


class RoomJoinView(LoginRequiredMixin, TemplateView):
    template_name = "matrix/join.html"
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        matrix_user = models.MatrixUser.objects.get(user=self.request.user.pk)
        rooms = []
        for room in models.ManagedRoom.objects.all():
            rooms.append(
                {
                    "name": room.name,
                    "id": room.pk,
                    "invited": models.UserInvitation.objects.filter(
                        user=matrix_user, room=room
                    ).exists(),
                }
            )

        context["matrix_user"] = matrix_user
        context["rooms"] = rooms
        return context

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and not models.MatrixUser.objects.filter(user=self.request.user.pk).exists()
        ):
            return redirect("matrix:matrix-user")
        return super(RoomJoinView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        room_id = request.POST.get("room_id", False)
        matrix_user = models.MatrixUser.objects.get(user=self.request.user.pk)
        if not room_id:
            return redirect("")
        room = None
        try:
            room = models.ManagedRoom.objects.get(pk=room_id)
        except models.ManagedRoom.DoesNotExist:
            return redirect("matrix:join")

        if models.UserInvitation.objects.filter(room=room, user=matrix_user).exists():
            return redirect("matrix:join")

        invite = models.UserInvitation()
        invite.room = room
        invite.user = matrix_user
        invite.save()
        invite.emit_invitation()
        return redirect("matrix:join")
