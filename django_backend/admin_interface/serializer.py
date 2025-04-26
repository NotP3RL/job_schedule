from .models import Employee


def check_telegram_id(id):
    if Employee.objects.get(telegram_id=id):
        return True
    else:
        return False