from django.urls import path
from django.views.generic import TemplateView

app_name = "profile"

urlpatterns = [
    path("", TemplateView.as_view(template_name="profile/settings.html"), name="settings"),
    path("change-password/", TemplateView.as_view(template_name="profile/change_password.html"), name="change_password"),
    # موقت: فرم تنظیمات به همین صفحه برمی‌گرده
    path("update-dormitory/", TemplateView.as_view(template_name="profile/settings.html"), name="update_dormitory"),
]