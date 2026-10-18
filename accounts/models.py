from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .utils import normalize_answer


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, student_id, password=None, **extra):
        if not student_id:
            raise ValueError("شماره دانشجویی الزامی است.")
        user = self.model(student_id=student_id, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(student_id, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    student_id = models.CharField("شماره دانشجویی", max_length=20, unique=True)
    full_name = models.CharField("نام و نام خانوادگی", max_length=150)

    # سؤال امنیتی برای بازیابی رمز؛ پاسخ مثل رمز عبور هش می‌شه، نه متن ساده
    security_question = models.CharField(max_length=255, blank=True)
    security_answer_hash = models.CharField(max_length=128, blank=True)
    failed_reset_attempts = models.PositiveSmallIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

    def set_security_answer(self, raw_answer):
        self.security_answer_hash = make_password(normalize_answer(raw_answer))

    def check_security_answer(self, raw_answer):
        return check_password(normalize_answer(raw_answer), self.security_answer_hash)