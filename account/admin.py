from django.contrib import admin
from .models import UserProfile, UserInfo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'StudentID', 'phone')
    list_filter = ("phone",)

admin.site.register(UserProfile, UserProfileAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", 'school', 'profession', 'address', 'aboutme', 'photo')
    list_filter = ("school", "profession")

admin.site.register(UserInfo, UserInfoAdmin)