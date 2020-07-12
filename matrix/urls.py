from django.urls import path
from django.views.generic import TemplateView, RedirectView
from . import views
from django.urls import reverse_lazy

app_name = "matrix"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("matrix:join"))),
    path("login", TemplateView.as_view(template_name="matrix/login.html")),
    path("matrix-user", views.UserCreationView.as_view(), name="matrix-user"),
    path("join", views.JoinView.as_view(), name="join"),
]
