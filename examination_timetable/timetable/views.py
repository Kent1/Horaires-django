from django.template import Context, loader
from django.shortcuts import render, render_to_response
from timetable.models import Timetable

# Create your views here.

def student(request, student_id):
    t = Timetable.objects.all()
    return render_to_response('timetable.html',
                                {'id': student_id,
                                'timetable' : t})

def professor(request, professor_id):
    return render_to_response('timetable.html',
                                {'id' : professor_id,
                                })
