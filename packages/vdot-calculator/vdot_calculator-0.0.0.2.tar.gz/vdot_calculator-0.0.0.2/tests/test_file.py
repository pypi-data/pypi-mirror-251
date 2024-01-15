import src.vdot_calculator.func_module as vdot
import datetime


def test_direct_de_35_igual_25():
    assert abs(vdot.direct(35, 5000) - 25.5) <= 0.1

def test_direct_de_35_igual_25_por_time_pace():
    time = datetime.time(minute=35, second=00)
    pace = datetime.time(minute=7, second=00)
    v_dot = vdot.vdot_from_time_and_pace(time, pace)
    error = abs(v_dot - 25.5)
    assert error <= 0.1


def test_direct_de_30_igual_30():
    pace = datetime.time(minute=5, second=7)
    distance = 10000  # m
    error = vdot.vdot_from_distance_and_pace(distance, pace) - 39
    assert abs(error) <= 0.1


def test_direct_de_27_igual_35():
    total_time = datetime.time(minute=27, second=00)
    total_time_minutes = vdot.convert_to_minutes(total_time)
    distance = 5000  # m
    error = vdot.direct(total_time_minutes, distance) - 35
    assert abs(error) <= 0.1

def test_5000m_and_2408():
    distance = 5000 # meters
    time = datetime.time(minute=24, second=8)
    v_dot = vdot.vdot_from_time_and_distance(time, distance)
    error = abs(v_dot-40)
    assert error <= 0.1