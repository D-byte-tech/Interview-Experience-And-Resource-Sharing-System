from django.contrib import admin
from Interview.models import InterviewDatabase
from Interview.models import TestUser
from Interview.models import ResourceDatabase
from Interview.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomizedUserAdmin (UserAdmin):
    inlines = (ProfileInline, )

    
admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)


admin.site.register(InterviewDatabase)
admin.site.register(TestUser)
admin.site.register(ResourceDatabase)

