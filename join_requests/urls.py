from django.urls import path
from django.views.generic import TemplateView

app_name = "requests"

urlpatterns = [
    path("", TemplateView.as_view(template_name="requests/list.html"), name="list"),
]