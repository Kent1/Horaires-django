from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def _create_user(self, password, is_admin, is_superuser, **extra_fields):
        user = self.model(is_admin=is_admin, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(password, False, False, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        return self._create_user(password, True, True, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    matricule = models.IntegerField(unique=True, primary_key=True)

    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=30)
    email      = models.EmailField(blank=True)

    is_admin = models.BooleanField(
        'admin status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
        )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as \
                  active. Unselect this instead of deleting accounts.'
        )

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    USERNAME_FIELD  = 'matricule'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __unicode__(self):
        return '%s (%d)' % (self.get_full_name(), self.matricule)


class Professor(MyUser):
    pass


class Unavailability(models.Model):
    class Meta:
        verbose_name_plural = 'Unavailabities'

    professor = models.ForeignKey(Professor)
    date      = models.DateField()
    matin     = models.BooleanField()


class Student(MyUser):
    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self.is_active = False


class Faculty(models.Model):
    class Meta:
        verbose_name_plural = 'faculties'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    name      = models.CharField(max_length=100)
    faculty   = models.ForeignKey(Faculty)
    capacity  = models.IntegerField()
    room_type = models.ForeignKey(RoomType)

    def __unicode__(self):
        return self.name


class Exam(models.Model):
    name         = models.CharField(max_length=100)
    faculty      = models.ForeignKey(Faculty)
    room_type    = models.ForeignKey(RoomType)
    professor    = models.ForeignKey(Professor)
    students     = models.ManyToManyField(Student)
    room         = models.OneToOneField(Room, null=True)
    timeslot     = models.IntegerField(null=True)
    conflicts    = models.IntegerField(null=True)
    dependencies = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Timetable(models.Model):
    start = models.DateField()
    end   = models.DateField()
    exams = models.ManyToManyField(Exam)
    rooms = models.ManyToManyField(Room)
