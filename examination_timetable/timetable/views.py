from django.template import Context, loader
from django.shortcuts import render, render_to_response
from timetable.models import Student, Professor, Exam

# Create your views here.

def student(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render_to_response('timetable.html',
                                {'id': student_id,
                                 'first_name' : student.first_name,
                                 'last_name' : student.last_name
                                 })

def professor(request, professor_id):
    professor = Professor.objects.get(pk=professor_id)
    return render_to_response('timetable.html',
                                {'id' : professor_id,
                                 'first_name' : professor.first_name,
                                 'last_name' : professor.last_name
                                })

def exam(request, exam_id):
    exam = Exam.objects.get(pk=exam_id)
    return render_to_response('exam.html',
                                {
                                    'exam' : exam,
                                })
