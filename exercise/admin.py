from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Blog, Exercise


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profile'
    fk_name = 'user'


# managed in the same way as profileinline
class ExerciseInline(admin.StackedInline):
    model = Exercise
    can_delete = True
    verbose_name_plural = 'Exercises'


# created admin to manage blog posts and see if they are reaching the database
class BlogAdmin(admin.ModelAdmin):
    model = Blog


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, ExerciseInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(Blog, BlogAdmin)
admin.site.register(User, CustomUserAdmin)
