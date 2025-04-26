from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Employee, Shift, Break, Weekend, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    readonly_fields = ['display_title', 'display_date', 'display_description']
    exclude = ['title', 'date', 'description']

    @admin.display(description='название')
    def display_title(self, obj):
        return obj.title

    @admin.display(description='дата')
    def display_date(self, obj):
        return obj.date

    @admin.display(description='описание')
    def display_description(self, obj):
        return obj.description


class ShiftInline(admin.TabularInline):
    model = Shift
    readonly_fields = ['display_start_time', 'display_end_time', 'display_image']
    exclude = ['image', 'status']

    @admin.display(description='начальное время')
    def display_start_time(self, obj):
        return obj.start_time

    @admin.display(description='конечное время')
    def display_end_time(self, obj):
        return obj.end_time

    @admin.display(description='изображение')
    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')





class WeekendInline(admin.TabularInline):
    model = Weekend
    readonly_fields = ['display_start_date', 'display_end_date']
    exclude = ['start_date', 'end_date']

    @admin.display(description='начальная дата')
    def display_start_date(self, obj):
        return obj.start_date

    @admin.display(description='конечная дата')
    def display_end_date(self, obj):
        return obj.end_date


class BreakInline(admin.TabularInline):
    model = Break
    readonly_fields = ['display_start_time', 'display_end_time']
    exclude = ['status']

    @admin.display(description='начальное время')
    def display_start_time(self, obj):
        return obj.start_time

    @admin.display(description='конечное время')
    def display_end_time(self, obj):
        if obj.status:
            return obj.end_time
        else:
            return 'смена не закончена'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        TicketInline,
        ShiftInline,
        WeekendInline
    ]
    list_display = ['display_name', 'display_telegram_id', 'last_shift', 'last_ticket',  'last_weekend']

    @admin.display(description='имя')
    def display_name(self, obj):
        return obj.name

    @admin.display(description='телеграмм')
    def display_telegram_id(self, obj):
        return obj.telegram_id

    @admin.display(description='последняя смена')
    def last_shift(self, obj):
        return Shift.objects.filter(employee=obj).latest('id')

    @admin.display(description='последний штраф')
    def last_ticket(self, obj):
        return Ticket.objects.filter(employee=obj).latest('id')

    @admin.display(description='последний выходной')
    def last_weekend(self, obj):
        return Weekend.objects.filter(employee=obj).latest('id')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    inlines = [BreakInline]
    list_display = ['display_start_time', 'display_end_time', 'employee_telegram_id']

    @admin.display(description='начальное время')
    def display_start_time(self, obj):
        return obj.start_time

    @admin.display(description='конечное время')
    def display_end_time(self, obj):
        if obj.status:
            return obj.end_time
        else:
            return 'смена не закончена'

    @admin.display(description='telegram id сотрудника')
    def employee_telegram_id(self, obj):
        return obj.employee.telegram_id


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ['display_start_time', 'display_end_time', 'display_shift']

    @admin.display(description='начальное время')
    def display_start_time(self, obj):
        return obj.start_time

    @admin.display(description='конечное время')
    def display_end_time(self, obj):
        if obj.status:
            return obj.end_time
        else:
            return 'смена не закончена'

    @admin.display(description='смена')
    def display_shift(self, obj):
        return obj.shift


@admin.register(Weekend)
class WeekendAdmin(admin.ModelAdmin):
    list_display = ['display_start_date', 'display_end_date', 'employee_telegram_id']

    @admin.display(description='начальная дата')
    def display_start_date(self, obj):
        return obj.start_date

    @admin.display(description='конечная дата')
    def display_end_date(self, obj):
        return obj.end_date

    @admin.display(description='telegram id сотрудника')
    def employee_telegram_id(self, obj):
        return obj.employee.telegram_id


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['display_title', 'employee_telegram_id', 'display_date', 'display_description']

    @admin.display(description='имя')
    def display_title(self, obj):
        return obj.title

    @admin.display(description='telegram id сотрудника')
    def employee_telegram_id(self, obj):
        return obj.employee.telegram_id

    @admin.display(description='дата')
    def display_date(self, obj):
        return obj.date

    @admin.display(description='описание')
    def display_description(self, obj):
        return obj.description
    


# Register your models here.
