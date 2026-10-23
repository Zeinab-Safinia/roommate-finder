import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegisterForm
from .models import User
from .utils import normalize_digits

MAX_RESET_ATTEMPTS = 3      # حداکثر پاسخ اشتباه به سؤال امنیتی
RESET_WINDOW_SECONDS = 600  # بعد از تأیید پاسخ، ۱۰ دقیقه فرصت تعیین رمز جدید


def register_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("onboarding:select_dormitory")
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = LoginForm(request, request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.user)
        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}
        ):
            return redirect(next_url)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "accounts/login.html", {"form": form})


def password_reset_view(request):
    ctx = {"step": "find_question"}

    if request.method == "POST":
        # مرحلهٔ ۲: تعیین رمز جدید (فقط اگه پاسخ سؤال امنیتی قبلاً تأیید شده)
        if "new_password" in request.POST:
            uid = request.session.get("reset_user_id")
            verified_at = request.session.get("reset_verified_at", 0)
            if not uid or time.time() - verified_at > RESET_WINDOW_SECONDS:
                messages.error(request, "مهلت بازیابی تمام شده. دوباره شروع کن.")
                return redirect("accounts:password_reset")

            p1 = request.POST.get("new_password", "")
            p2 = request.POST.get("new_password_confirm", "")
            ctx["step"] = "set_password"
            if p1 != p2:
                messages.error(request, "رمز جدید و تکرار آن یکسان نیست.")
            else:
                try:
                    validate_password(p1)
                except ValidationError as e:
                    for msg in e.messages:
                        messages.error(request, msg)
                else:
                    user = User.objects.get(pk=uid)
                    user.set_password(p1)
                    user.failed_reset_attempts = 0
                    user.save()
                    request.session.pop("reset_user_id", None)
                    request.session.pop("reset_verified_at", None)
                    messages.success(request, "رمز عبور تغییر کرد. حالا وارد شو.")
                    return redirect("accounts:login")

        # مرحلهٔ ۱: پیدا کردن کاربر، نمایش و بررسی سؤال امنیتی
        else:
            sid = normalize_digits(request.POST.get("student_id", ""))
            user = User.objects.filter(student_id=sid).first()
            if user is None:
                messages.error(request, "شماره دانشجویی پیدا نشد.")
            elif user.failed_reset_attempts >= MAX_RESET_ATTEMPTS:
                messages.error(
                    request, "تعداد تلاش‌های اشتباه زیاد بود. با مدیر سامانه تماس بگیر."
                )
            else:
                ctx["student_id"] = sid
                ctx["security_question"] = user.security_question
                answer = request.POST.get("security_answer")
                if answer is not None:
                    if user.check_security_answer(answer):
                        request.session["reset_user_id"] = user.pk
                        request.session["reset_verified_at"] = time.time()
                        ctx["step"] = "set_password"
                    else:
                        user.failed_reset_attempts += 1
                        user.save(update_fields=["failed_reset_attempts"])
                        messages.error(request, "پاسخ اشتباه است.")

    return render(request, "accounts/password_reset.html", ctx)