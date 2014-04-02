from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

import models


class ExamForm(forms.ModelForm):
    forms.BooleanField()

    class Meta:
        model = models.Exam
        help_texts = {
            'name': '',
            'faculty': 'Faculty which organizes the exam.',
            'room_type': 'Choose the correct room type for the exam',
            'professor': 'Which professor gives this course ?',
            'students': '',
        }


class RoomForm(forms.ModelForm):

    class Meta:
        model = models.Room
        help_texts = {
            'name': '',
            'faculty': 'Choose the faculty which owns the room.',
            'capacity': 'What is the number of seatings in the room ?',
            'room_type': 'Choose what is the type of the room.',
        }


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.MyUser
        fields = ('matricule', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.MyUser
        fields = ['matricule', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UnavailabilityForm(forms.ModelForm):
    CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon')
    ]

    ampm = forms.ChoiceField(label='AM/PM', choices=CHOICES,
                             initial='morning', widget=forms.RadioSelect())

    class Meta:
        model = models.Unavailability
        fields = ['professor', 'date', 'ampm']


class TimetableForm(forms.ModelForm):

    class Meta:
        model = models.Timetable

    def clean_start(self):
        start = self.cleaned_data['start']
        if start.weekday() == 5 or start.weekday() == 6:
            raise forms.ValidationError(
                "Do you really start exam session a weekend ?")
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        if end.weekday() == 5 or end.weekday() == 6:
            raise forms.ValidationError(
                "Do you really end exam session a weekend ?")
        return end
