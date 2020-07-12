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


class JoinView(LoginRequiredMixin, TemplateView):
    template_name = "matrix/join.html"
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        matrix_user = models.MatrixUser.objects.get(user=self.request.user.pk)
        communities = []
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
        for com in models.ManagedCommunity.objects.all():
            communities.append(
                {
                    "name": com.friendly_name,
                    "id": com.pk,
                    "invited": models.CommunityUserInvitation.objects.filter(
                        user=matrix_user, community=com
                    ).exists(),
                }
            )

        context["matrix_user"] = matrix_user
        context["rooms"] = rooms
        context["communities"] = communities
        return context

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and not models.MatrixUser.objects.filter(user=self.request.user.pk).exists()
        ):
            return redirect("matrix:matrix-user")
        return super(JoinView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        room_id = request.POST.get("room_id", False)
        community_id = request.POST.get("community_id", False)
        matrix_user = models.MatrixUser.objects.get(user=self.request.user.pk)

        if community_id == room_id:
            return redirect("matrix:join")

        if room_id:
            return self.post_invite(
                models.ManagedRoom, models.UserInvitation, matrix_user, room_id
            )
        if community_id:
            return self.post_invite(
                models.ManagedCommunity,
                models.CommunityUserInvitation,
                matrix_user,
                community_id,
            )

        return redirect("matrix:join")

    def post_invite(self, container_class, invite_class, matrix_user, cid):
        obj = None
        try:
            obj = container_class.objects.get(pk=cid)
        except container_class.DoesNotExist:
            return redirect("matrix:join")

        req_dict = {invite_class.resource_name: obj, "user": matrix_user}
        if invite_class.objects.filter(**req_dict).exists():
            return redirect("matrix:join")

        invite = invite_class(**req_dict)
        invite.save()
        invite.emit_invitation()
        return redirect("matrix:join")
