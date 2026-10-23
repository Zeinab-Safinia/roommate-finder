from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "is_staff", "date_joined")
    search_fields = ("student_id", "full_name")
    readonly_fields = ("password", "security_answer_hash", "last_login", "date_joined")
    exclude = ("groups", "user_permissions")

    def has_add_permission(self, request):
        # کاربر جدید فقط از صفحهٔ ثبت‌نام ساخته بشه (رمز درست هش بشه)
        return False