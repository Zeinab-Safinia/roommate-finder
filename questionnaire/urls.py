from django.urls import path
from django.views.generic import TemplateView

app_name = "questionnaire"

urlpatterns = [
    path("lifestyle/", TemplateView.as_view(template_name="questionnaire/lifestyle.html"), name="lifestyle"),
    path("personality/", TemplateView.as_view(template_name="questionnaire/personality.html"), name="personality"),
]