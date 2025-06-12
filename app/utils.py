import re


def validate_email(email):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None


def validate_phone(phone: str) -> bool:
    regex = r"^\(\d{2}\) 9\d{4}-\d{4}$"
    return re.match(regex, phone) is not None
