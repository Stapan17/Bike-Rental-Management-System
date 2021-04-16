from django.contrib import admin
from .models import userInfo, User, Bike, Rent, Station, Employee, Payment, contactUS

admin.site.register(userInfo)
admin.site.register(Bike)
admin.site.register(Rent)
admin.site.register(Station)
admin.site.register(Employee)
admin.site.register(Payment)
admin.site.register(contactUS)
