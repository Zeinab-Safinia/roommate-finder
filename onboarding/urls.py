from django.urls import path
from django.views.generic import TemplateView

app_name = "onboarding"

urlpatterns = [
    path("dormitory/", TemplateView.as_view(template_name="onboarding/select_dormitory.html"), name="select_dormitory"),
    path("building/", TemplateView.as_view(template_name="onboarding/select_building.html"), name="select_building"),
    path("group-status/", TemplateView.as_view(template_name="onboarding/group_status.html"), name="group_status"),
]