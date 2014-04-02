import datetime
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from timetable.models import Student, Professor, Exam, Timetable, Room

import util


def students(request):
    students = Student.objects.all()
    return render_to_response('list.html',
                                {
                                    'title' : 'Students',
                                    'url' : 'student',
                                    'list' : students
                                })

def student(request, student_id):
    timetable = Timetable.objects.all()
    timetable = timetable[0]
    student = Student.objects.get(pk=student_id)
    my_exam = list()
    exams = Exam.objects.all()
    for exam in exams:
        students = exam.students.all()
        for stud in students:
            if stud.pk == student.pk:
                convert_timeslot_to_date(exam, timetable)
                my_exam.append(exam)

    return render_to_response('timetable.html',
                                {'id': student_id,
                                 'first_name' : student.first_name,
                                 'last_name' : student.last_name,
                                 'timetable' : timetable,
                                 'exams' : my_exam
                                 })


def students(request):
    students = Student.objects.all()
    return render_to_response('list.html',
                                {
                                    'title' : 'Students',
                                    'url' : 'student',
                                    'list' : students
                                })

def professors(request):
    professors = Professor.objects.all()
    return render_to_response('list.html',
                                {
                                    'title' : 'Professors',
                                    'url' : 'professor',
                                    'list' : professors
                                })

def professor(request, professor_id):
    timetable = Timetable.objects.all()
    timetable = timetable[0]
    professor = Professor.objects.get(pk=professor_id)
    my_exam = list()
    exams = Exam.objects.all()
    for exam in exams:
        if exam.professor.pk == professor.pk:
            convert_timeslot_to_date(exam, timetable)
            my_exam.append(exam)
    return render_to_response('timetable.html',
                                {'id' : professor_id,
                                 'first_name' : professor.first_name,
                                 'last_name' : professor.last_name,
                                 'timetable' : timetable,
                                 'exams' : my_exam
                                })

def exam(request, exam_id):
    exam = Exam.objects.get(pk=exam_id)
    return render_to_response('exam.html',
                                {
                                    'exam' : exam,
                                })

def exams(request):
    timetable = Timetable.objects.all()
    timetable = timetable[0]
    exams = Exam.objects.all()
    for exam in exams:
        convert_timeslot_to_date(exam, timetable)
    return render_to_response('exams.html',
                                {
                                    'exams' : exams,
                                    'timetable' : timetable,
                                })

def room(request, room_id):
    timetable = Timetable.objects.all()
    timetable = timetable[0]
    room = Room.objects.get(pk=room_id)
    my_exam = list()
    exams = Exam.objects.all()
    for exam in exams:
        if exam.room.pk == room.pk:
            convert_timeslot_to_date(exam, timetable)
            my_exam.append(exam)
    return render_to_response('timetable.html',
                                {
                                    'id' : room.pk,
                                    'first_name' : room.name,
                                    'last_name' : '',
                                    'timetable' : timetable,
                                    'exams' : my_exam
                                })

def rooms_list(request):
    rooms = Room.objects.all()
    return render_to_response('list.html',
                                {
                                    'title' : 'Rooms',
                                    'url' : 'room',
                                    'list' : rooms
                                })

def index(request):
    rooms = Room.objects.all()
    professors = Professor.objects.all()
    students = Student.objects.all()
    exams = Exam.objects.all()
    return render_to_response('index.html',
                                {
                                    'rooms' : rooms,
                                    'students' : students,
                                    'professors' : professors,
                                    'exams' : exams
                                })


def convert_timeslot_to_date(exam, timetable):
    exam.date = timetable.start + datetime.timedelta(
        days=(util.get_day_delta(timetable.start, exam.timeslot)))
    time = exam.date.timetuple()
    exam.month = time.tm_mon - 1
    exam.day = time.tm_mday
    exam.m_start = 15
    exam.m_end = 15
    if exam.timeslot % 2 == 0:
        exam.h_start = 8
        exam.h_end = 12
    else:
        exam.h_start = 13
        exam.h_end = 17
