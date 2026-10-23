from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator

from .models import User
from .utils import normalize_digits

student_id_validator = RegexValidator(
    r"^\d{6,12}$", "شماره دانشجویی باید فقط عدد (۶ تا ۱۲ رقم) باشد."
)


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    student_id = forms.CharField(max_length=20)
    password = forms.CharField(strip=False)
    password_confirm = forms.CharField(strip=False)
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)

    def clean_student_id(self):
        sid = normalize_digits(self.cleaned_data["student_id"])
        student_id_validator(sid)
        # sql (WHERE student_id = 'sid')
        if User.objects.filter(student_id=sid).exists(): 
            raise forms.ValidationError("این شماره دانشجویی قبلاً ثبت‌نام کرده است.")
        return sid

    def clean(self):
        data = super().clean()
        p1, p2 = data.get("password"), data.get("password_confirm")
        if p1 and p2 and p1 != p2:
            self.add_error("password_confirm", "رمز عبور و تکرار آن یکسان نیست.")
        elif p1:
            try:
                validate_password(p1)
            except forms.ValidationError as e:
                self.add_error("password", e)
        return data

    def save(self):
        d = self.cleaned_data
        user = User.objects.create_user(
            student_id=d["student_id"],
            password=d["password"],
            full_name=d["full_name"],
            security_question=d["security_question"].strip(),
        )
        user.set_security_answer(d["security_answer"])
        user.save()
        return user


class LoginForm(forms.Form):
    student_id = forms.CharField()
    password = forms.CharField(strip=False)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        sid, pw = data.get("student_id"), data.get("password")
        if sid and pw:
            self.user = authenticate(
                self.request, username=normalize_digits(sid), password=pw
            )
            if self.user is None:
                raise forms.ValidationError("شماره دانشجویی یا رمز عبور اشتباه است.")
        return data