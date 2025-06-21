from django.contrib import admin
from .models import Class, Instructor, Bookings

# Register your models here.
admin.site.register(Class)
admin.site.register(Instructor)
admin.site.register(Bookings)