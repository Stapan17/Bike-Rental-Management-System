from django.contrib import admin
from .models import userInfo, User, Bike, Rent

admin.site.register(userInfo)
admin.site.register(Bike)
admin.site.register(Rent)
