import datetime
import os
import random

def get_time():
    hr_val = random.randrange(10, 21, 1)
    min_val = random.randrange(10, 59, 1)
    time_string = str(hr_val) + ':' + str(min_val)
    return time_string

def get_current_time():
    current_time = datetime.datetime.now()
    current_time_string = str(current_time.hour) + ':' + str(current_time.minute)
    return current_time_string

def time_compare():
    guess_time = get_time()
    current_time = get_current_time()

    if guess_time == current_time:
        return True
    else:
        return False
