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
