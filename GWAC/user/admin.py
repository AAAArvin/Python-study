from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'is_superuser', 'user_level', 'company')

    def user_level(self, obj):
        return obj.profile.user_level
    user_level.short_description = '用户等级'
    def company(self, obj):
        return obj.profile.company
    company.short_description = '所属单位'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_level', 'company', 'tel')