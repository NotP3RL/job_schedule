from datetime import date, datetime
from django.core.files import File
import requests
from io import BytesIO
from .models import Employee, Shift, Break, Weekend


# Проверка, зарегистрирован ли сотрудник с указанным telegram_id
def check_telegram_id(id):
    if Employee.objects.filter(telegram_id=id).exists():
        return True
    else:
        return False


# Проверка, есть ли незавершённая смена у сотрудника сегодня
def check_shift_status(id):
    employee = Employee.objects.get(telegram_id=id)
    if Shift.objects.filter(employee=employee, start_time__date=date.today(), status=False).exists():
        return True
    else:
        return False


# Проверка, есть ли незавершённый перерыв у сотрудника в текущей смене
def check_break_status(id):
    employee = Employee.objects.get(telegram_id=id)
    shift = Shift.objects.get(employee=employee, start_time__date=date.today(), status=False)
    if Break.objects.filter(shift=shift, status=False).exists():
        return True
    else:
        return False


# Создание новой смены с загрузкой фотографии рабочего места
def create_new_shift(id, image_url):
    employee = Employee.objects.get(telegram_id=id)
    image = requests.get(image_url, stream=True)
    img_file = BytesIO(image.content)
    django_file = File(img_file, name='image.jpg')
    if Shift.objects.filter(employee=employee, start_time__date=date.today()).exists():
        shift = Shift.objects.get(employee=employee, start_time__date=date.today(), status=True)
        shift.status = False
        shift.save()
    else:
        Shift.objects.create(employee=employee, image=django_file)


# Завершение текущей смены
def end_new_shift(id):
    employee = Employee.objects.get(telegram_id=id)
    shift = Shift.objects.get(employee=employee, status=False)
    shift.status = True
    shift.save()


# Создание нового перерыва в рамках текущей смены
def create_new_break(id):
    employee = Employee.objects.get(telegram_id=id)
    shift = Shift.objects.get(employee=employee, status=False)
    Break.objects.create(shift=shift)


# Завершение текущего перерыва
def end_shift_break(id):
    employee = Employee.objects.get(telegram_id=id)
    shift = Shift.objects.get(employee=employee, status=False)
    shift_break = Break.objects.get(shift=shift, status=False)
    shift_break.status = True
    shift_break.save()


# Проверка возможности установить выходной день
def check_weekend(id, text_message):
    weekend_date = datetime.strptime(text_message, "%d/%m/%Y").date()
    employee = Employee.objects.get(telegram_id=id)
    employees = Employee.objects.all()
    if weekend_date - date.today() < 2:
        return False
    if employees.count() < 2:
        return False
    elif Weekend.objects.filter(date=weekend_date, employee=employee).exists():
        return False
    else:
        k = employees.count()-1
        weekend = Weekend.objects.filter(date=weekend_date)
        if weekend < k:
            return True


# Получение всех предстоящих выходных сотрудника (не реализовано полностью)
def see_weekends(id):
    employee = Employee.objects.get(telegram_id=id)
    weekends = Weekend.objects.filter(employee=employee, date__gte=date.today())
    # filtered_weekends = []
    # for weekend in weekends:
    #     if weekend.date > date.today()
    return weekends





def create_weekend(id, text_message):
    date = datetime.strptime(text_message, "%d/%m/%Y").date()
    employee = Employee.objects.get(telegram_id=id)
    Weekend.objects.create(date=date, employee=employee)