from django.urls import path
from django.views.generic import TemplateView

app_name = "chat"

urlpatterns = [
    path("<int:room_id>/", TemplateView.as_view(template_name="chat/room.html"), name="room"),
]