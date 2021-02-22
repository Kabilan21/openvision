from django.contrib import admin

from .models import User, Attendance, UnknownModel

admin.site.register(User)
admin.site.register(Attendance)
admin.site.register(UnknownModel)
