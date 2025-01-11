from django.contrib import admin

from boostlab_employees.models import Employee,Department,Manager

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Manager)