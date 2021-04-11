from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Blog, SportsXP, Exercise, Bmi


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class SportsXPInline(admin.StackedInline):
    model = SportsXP
    can_delete = True
    verbose_name_plural = 'SportsXP'
    fk_name = 'user'

# managed in the same way as profileinline


class ExerciseInline(admin.StackedInline):
    model = Exercise
    can_delete = True
    verbose_name_plural = 'Exercises'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, SportsXPInline, ExerciseInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile


class BlogAdmin(admin.ModelAdmin):
    model = Blog


class SportsXPAdmin(admin.ModelAdmin):
    model = SportsXP


class BlogAdmin(admin.ModelAdmin):
    model = Blog


class ExerciseAdmin(admin.ModelAdmin):
    model = Exercise

class BmiAdmin(admin.ModelAdmin):
    model = Bmi


admin.site.unregister(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(SportsXP, SportsXPAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Bmi, BmiAdmin)
