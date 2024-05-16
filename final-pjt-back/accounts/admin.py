from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username', 'age', 'gender', 'salary', 'wealth', 'period')
    fields = ('userid', 'password', 'username', 'age', 'gender', 'salary', 'wealth', 'period')

admin.site.register(User, UserAdmin)