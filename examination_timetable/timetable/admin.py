from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

import models
import forms

admin.site.register(models.Faculty)
admin.site.register(models.RoomType)


class ExamAdmin(admin.ModelAdmin):
    form = forms.ExamForm
    list_display = ('name', 'faculty', 'professor')
    #fields = ['name', 'faculty', 'room_type', 'professor', 'students']
    fieldsets = (
        (None, {'fields': ('name', 'faculty')}),
        ('Participants', {'fields': ('professor', 'students')}),
        ('Room', {'fields': ('room_type',)}),
        #('Schedule', {'fields': ('timeslot', 'room')}),
        #('Availabilities', {'fields': ('availabilities',)}),
        ('Dependencies', {'fields': ('dependencies',)}),
    )

admin.site.register(models.Exam, ExamAdmin)


class RoomAdmin(admin.ModelAdmin):
    form = forms.RoomForm
    list_display = ('name', 'faculty', 'capacity', 'room_type')

admin.site.register(models.Room, RoomAdmin)


class ProfessorAdmin(UserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('matricule', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('matricule', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'matricule',
                # 'password1',
                # 'password2',
                'first_name',
                'last_name'
            )}
        ),
    )
    search_fields = ('matricule',)
    ordering = ('matricule',)
    filter_horizontal = ()


class StudentAdmin(UserAdmin):
    # The forms to add and change user instances
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('matricule', 'first_name', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('matricule', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'matricule',
                # 'password1',
                # 'password2',
                'first_name',
                'last_name'
            )}
        ),
    )
    search_fields = ('matricule',)
    ordering = ('matricule',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(models.Professor, ProfessorAdmin)


class UnavailabilityAdmin(admin.ModelAdmin):
    form = forms.UnavailabilityForm


def make_schedule(modeladmin, request, queryset):
    for timetable in queryset:
        timetable.schedule()
    queryset.update()
make_schedule.short_description = "Schedule the selected timetable"


class TimetableAdmin(admin.ModelAdmin):
    form = forms.TimetableForm
    actions = [make_schedule]

admin.site.register(models.Timetable, TimetableAdmin)

admin.site.register(models.Unavailability, UnavailabilityAdmin)
admin.site.register(models.Student, StudentAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
