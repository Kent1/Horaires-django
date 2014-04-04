import datetime
from django.template import Context, loader
from django.shortcuts import render, render_to_response
from timetable.models import Student, Professor, Exam, Timetable, Room

import util

def student(request, student_id):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    student = Student.objects.get(pk=student_id)
    my_exam = list()
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
                                    'title' : 'Student',
                                    'url' : 'student',
                                    'list' : students
                                })

def professors(request):
    professors = Professor.objects.all()
    return render_to_response('list.html',
                                {
                                    'title' : 'Professor',
                                    'url' : 'professor',
                                    'list' : professors
                                })

def professor(request, professor_id):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    professor = Professor.objects.get(pk=professor_id)
    my_exam = list()
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
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    for exam in exams:
        print exam.timeslot
        convert_timeslot_to_date(exam, timetable)
    return render_to_response('exams.html',
                                {
                                    'exams' : exams,
                                    'timetable' : timetable,
                                })

def all_exams(request):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')

    colors = []
    last_color = [0, 0, 0, 0]
    for exam in exams:
        convert_timeslot_to_date(exam, timetable)
        assign_color(exam, colors, last_color)

    return render_to_response('all_exams.html',
                                {
                                    'timetable' : timetable,
                                    'exams' : exams
                                })

def room(request, room_id):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
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
                                    'title' : 'Room',
                                    'url' : 'room',
                                    'list' : rooms
                                })

def index(request):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    rooms = Room.objects.all()
    professors = Professor.objects.all()
    students = Student.objects.all()
    return render_to_response('index.html',
                                {
                                    'rooms' : rooms,
                                    'students' : students,
                                    'professors' : professors,
                                    'exams' : exams
                                })


def convert_timeslot_to_date(exam, timetable):
    real_timeslot = exam.timeslot - timetable.start.weekday()*2

    exam.date = timetable.start + datetime.timedelta(
        days=(util.get_day_delta(timetable.start, real_timeslot)))
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

def assign_color(exam, colors, last_color):
    assignation = False
    list_exam_studs = exam.students.all()

    for students, color in colors:
        counter = 0.0
        list_studs = students.all()

        for student in list_exam_studs:
            if student in list_studs:
                counter += 1

        if counter/len(list_exam_studs) > 0.8:
            exam.color = color
            assignation = True

    if not assignation:
        if last_color[-1] == 0:
            last_color[0] += (255 - last_color[0])/3
        elif last_color[-1] == 1:
            last_color[1] = last_color[0]*2
        else:
            last_color[2] = last_color[1]
        last_color[-1] = (last_color[-1]+1)%3

        color = 'rgb(%d,%d,%d)' % tuple(last_color[:3])
        colors.append((exam.students, color))
        exam.color = color
