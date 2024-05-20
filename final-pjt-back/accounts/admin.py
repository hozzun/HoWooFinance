from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'age', 'gender', 'salary', 'wealth', 'period')
    fields = ('username', 'password', 'name', 'age', 'gender', 'salary', 'wealth', 'period')

admin.site.register(User, UserAdmin)