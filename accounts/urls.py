from django.urls import path
from django.views.generic import TemplateView

app_name = "accounts"

urlpatterns = [
    path("login/", TemplateView.as_view(template_name="accounts/login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="accounts/register.html"), name="register"),
    path("password-reset/", TemplateView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    # موقت: بعداً با LogoutView واقعی جایگزین می‌شه
    path("logout/", TemplateView.as_view(template_name="accounts/login.html"), name="logout"),
]