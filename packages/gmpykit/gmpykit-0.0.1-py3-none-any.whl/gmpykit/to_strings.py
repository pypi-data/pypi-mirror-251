import datetime


def percent(nb: float) -> str:
    """Format the number sent into a % number."""
    the_number = round(100 * nb, 2)
    the_string = "{: >6.2f}%".format(the_number)
    return the_string

def get_readable_number(number:float) -> str:
    """Convert the given number into a more readable string"""

    for x in ['', 'k', 'M', 'B']:
        if number < 1000.0:
            return str(round(number, 1)) + x
        number /= 1000.0
    return str(number) 


def convert_bytes(size: float) -> str:
    """Convert bytes to KB, or MB or GB"""
    for x in ["B", "kB", "MB", "GB", "TB"]:
        if size < 1000.0:
            return "%3.1f %s" % (size, x)
        size /= 1000.0
    raise Exception("This Exception should never happen")


def now() -> float:
    """Get current timestamp in seconds (number)."""
    return int(datetime.datetime.now().timestamp())


def format_time(time: float) -> str:
    """Transform a number of second into a human readable string."""

    # Calculations
    hours = int(time / 3600)
    minutes = int((time - (3600 * hours)) / 60)
    seconds = int(round(time - (60 * minutes + 3600 * hours)))

    # Stringify to right format
    hours_str = "{:0>2.0f}".format(hours)
    minutes_str = "{:0>2.0f}".format(minutes)
    seconds_str = "{:0>2.0f}".format(seconds)

    return f"[{hours_str}h{minutes_str}m{seconds_str}s]"
