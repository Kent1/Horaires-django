def day_per_we():
    return 2


def nbr_of_we(start, end):
    delta = end - start
    return ((delta.days + 1) + start.weekday()) / 7


def get_day_delta(start, timeslot):
    delta = start.weekday() + timeslot/2
    n_weekend = delta / 5
    return timeslot/2 + n_weekend * day_per_we()
