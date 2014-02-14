from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100)


class RoomType(models.Model):
    name = models.CharField(max_length=100)


class Room(models.Model):
    name      = models.CharField(max_length=100)
    faculty   = models.OneToOneField(Faculty)
    capacity  = models.IntegerField()
    room_type = models.OneToOneField(RoomType)


class Exam(models.Model):
    name           = models.CharField(max_length=100)
    faculty        = models.OneToOneField(Faculty)
    room_type      = models.OneToOneField(RoomType)
    teacher        = models.IntegerField()
    room           = models.OneToOneField(Room)
    timeslot       = models.IntegerField()
    availabilities = models.IntegerField()
    conflicts      = models.IntegerField()
    dependencies   = models.ForeignKey('self')


class Timetable(models.Model):
    timeslots = models.IntegerField()
    exams     = models.ManyToManyField(Exam)
    rooms     = models.ManyToManyField(Room)
