import math


def direct(time_minutes, total_distance):
    velocity = total_distance / time_minutes
    percent_max = 0.8 + 0.1894393 * math.e ** (-0.012778 * time_minutes) + \
        0.2989558 * math.e ** (-0.1932605 * time_minutes)
    vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity ** 2
    vo2max = vo2 / percent_max
    return vo2max


def vdot_from_distance_and_pace(distance, pace):
    pace_minutes = convert_to_minutes(pace)
    total_time = distance * pace_minutes / 1000  # transforms distance from
    # km to meters
    vdot = direct(total_time, distance)
    return vdot


def vdot_from_time_and_distance(time, distance):
    time_minutes = convert_to_minutes(time)
    vdot = direct(time_minutes, distance)
    return vdot


def vdot_from_time_and_pace(time, pace):
    time_minutes = convert_to_minutes(time)
    pace_minutes = convert_to_minutes(pace)
    distance = time_minutes / pace_minutes * 1000
    v_dot = direct(time_minutes, distance)
    return v_dot


def convert_to_minutes(time):
    time_minutes = time.minute + time.second / 60 + time.hour * 60
    return time_minutes
