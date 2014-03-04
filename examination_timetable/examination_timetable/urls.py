from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examination_timetable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^student/(?P<student_id>\d{6})/$', 'timetable.views.student'),
    url(r'^professor/(?P<professor_id>\d{6})/$', 'timetable.views.professor'),
    url(r'^exam/(?P<exam_id>\d+)/$', 'timetable.views.exam'),
    url(r'^admin/', include(admin.site.urls)),
)
