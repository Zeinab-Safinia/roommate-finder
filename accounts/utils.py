# تبدیل ارقام فارسی به انگلیسی و یکسان‌سازی متن پاسخ سؤال امنیتی
_PERSIAN = "۰۱۲۳۴۵۶۷۸۹"
_TABLE = {ord(c): str(i) for i, c in enumerate(_PERSIAN)}


def normalize_digits(text):
    return text.translate(_TABLE).strip()


def normalize_answer(text):
    text = text.translate(_TABLE)
    text = text.replace("ي", "ی").replace("ك", "ک")
    return " ".join(text.split()).lower()