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
                util.convert_timeslot_to_date(exam, timetable)
                my_exam.append(exam)

    return render_to_response('timetable.html',
                                {
                                 'title' : student.first_name + ' ' + student.last_name + '\'s',
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
            util.convert_timeslot_to_date(exam, timetable)
            my_exam.append(exam)
    return render_to_response('timetable.html',
                                {
                                 'title' : professor.first_name + ' ' + professor.last_name + '\'s',
                                 'timetable' : timetable,
                                 'exams' : my_exam
                                })

def exam(request, exam_id):
    exam = Exam.objects.get(pk=exam_id)
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    util.convert_timeslot_to_date(exam, timetable)
    return render_to_response('exam.html',
                                {
                                    'exam' : exam,
                                })

def exams(request):
    timetable, exams = util.last_timetable_scheduled(Timetable.objects.all())
    if timetable == None:
        return render_to_response('error.html')
    for exam in exams:
        util.convert_timeslot_to_date(exam, timetable)
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
        util.convert_timeslot_to_date(exam, timetable)
        util.assign_color(exam, colors, last_color)

    return render_to_response('timetable.html',
                                {
                                    'title' : 'All exams',
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
            util.convert_timeslot_to_date(exam, timetable)
            my_exam.append(exam)
    return render_to_response('timetable.html',
                                {
                                    'title' : room.name + '\'s',
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