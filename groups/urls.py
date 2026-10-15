from django.urls import path
from django.views.generic import TemplateView

app_name = "groups"

urlpatterns = [
    path("", TemplateView.as_view(template_name="groups/dashboard.html"), name="dashboard"),
    path("group/", TemplateView.as_view(template_name="groups/group_detail.html"), name="group_detail"),
    path("final/", TemplateView.as_view(template_name="groups/final_group.html"), name="final_group"),
]