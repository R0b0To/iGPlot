
import re

def toMs(time_duration):
    match = re.match(r'\+ (\d+):(\d+\.\d+)', time_duration)
    if match:
        minutes, seconds = map(float, match.groups())
        milliseconds = (minutes * 60 + seconds) * 1000
        print(f"{time_duration} is equivalent to {milliseconds} milliseconds")
        return milliseconds
    else:
        print(f"{time_duration}")
        return '0'
    
toMs('0')