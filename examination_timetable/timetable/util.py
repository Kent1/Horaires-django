import datetime

def day_per_we():
    return 1


def nbr_of_we(start, end):
    delta = end - start
    return ((delta.days + 1) + start.weekday()) / 7


def get_day_delta(start, timeslot):
    delta = start.weekday() + timeslot/2
    n_weekend = delta / (7 - day_per_we())
    return timeslot/2 + n_weekend * day_per_we()

def last_timetable_scheduled(timetable):
    if len(timetable) == 0 or timetable[0].exams.all()[0].timeslot == None:
        return None, None
    else:
        return timetable[0], timetable[0].exams.all()

def convert_timeslot_to_date(exam, timetable):
    real_timeslot = exam.timeslot - timetable.start.weekday()*2

    exam.date = timetable.start + datetime.timedelta(
        days=(get_day_delta(timetable.start, real_timeslot)))
    time = exam.date.timetuple()
    exam.month = time.tm_mon - 1
    exam.day = time.tm_mday
    exam.m_start = 15
    exam.m_end = 15
    if exam.timeslot % 2 == 0:
        exam.h_start = 8
        exam.h_end = 12
        exam.color = 'blue'
    else:
        exam.h_start = 13
        exam.h_end = 17
        exam.color = 'green'

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
