from django.contrib import admin
from .models import Login,Products,Category,Users,Cart

admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Login)
admin.site.register(Category)
admin.site.register(Cart)

# Register your models here.
