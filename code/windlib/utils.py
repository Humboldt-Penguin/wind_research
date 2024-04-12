import numpy as np
from datetime import datetime, timedelta, timezone


####################################################################################################
'''PRINTING'''


def print_dict(d: dict, indent=0, format_pastable=False, condense_arrays=True) -> None:
    """
    DESCRIPTION:
    ------------
        Cleaner way to print a dictionary, with option to condense numpy arrays.

    PARAMETERS:
    ------------
        d : dict
            The dictionary to print.
        indent : int
            The current indentation level.
        format_pastable : bool
            (Default False) If True, will format the output so that it can be directly pasted into Python code as an assignment to a variable. 
        condense_arrays : bool
            (Default True) If True, condenses numpy arrays into a shape descriptor rather than printing each element. 
    """
    for key, value in d.items():
        spacing = '\t' * indent
        key_repr = f"'{key}'" if isinstance(key, str) else key
        if isinstance(value, dict):
            print(f"{spacing}{key_repr}")
            print_dict(value, indent+1, format_pastable, condense_arrays)
        elif isinstance(value, np.ndarray) and condense_arrays:
            print(f"{spacing}{key_repr}")
            print(f"{spacing}\t<np.ndarray, shape={value.shape}>")
        elif format_pastable:
            value_repr = f"'{value}'" if isinstance(value, str) else value
            print(f"{spacing}{key_repr}: {value_repr!r},")
        else:
            value_repr = f"'{value}'" if isinstance(value, str) else value
            print(f"{spacing}{key_repr}")
            print(f"{spacing}\t{value_repr}")



import sys
def get_size(variable):
    """Calculate the total memory size of a variable, including the size of its contents if it is a container."""
    def size_of(obj, seen=None):
        """Helper function to calculate size recursively, handling cycles."""
        if seen is None:
            seen = set()
        object_id = id(obj)
        if object_id in seen:
            return 0
        seen.add(object_id)

        size = sys.getsizeof(obj)
        if isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(size_of(item, seen) for item in obj)
        elif isinstance(obj, dict):
            size += sum(size_of(k, seen) + size_of(v, seen) for k, v in obj.items())

        return size

    size_bytes = size_of(variable)

    if size_bytes < 1024:  # Less than 1 KB
        return f"{size_bytes} bytes"
    elif size_bytes < 1024**2:  # Less than 1 MB
        size_kb = size_bytes / 1024
        return f"{size_kb:.2f} KB"
    elif size_bytes < 1024**3:  # Less than 1 GB
        size_mb = size_bytes / (1024**2)
        return f"{size_mb:.2f} MB"
    else:  # 1 GB or more
        size_gb = size_bytes / (1024**3)
        return f"{size_gb:.2f} GB"



# def get_size(obj):
#     '''Recursively find size of objects in bytes'''
#     if isinstance(obj, dict):
#         return sum((get_size(v) for v in obj.values())) + sum((get_size(k) for k in obj.keys())) + sys.getsizeof(obj)
#     elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
#         return sum((get_size(i) for i in obj)) + sys.getsizeof(obj)
#     elif isinstance(obj, np.ndarray):
#         return obj.nbytes + sys.getsizeof(obj)
#     else:
#         return sys.getsizeof(obj)       
    



def print_sep(n=100):
    print()
    print('-' * n)
    print()





####################################################################################################
'''TIME DATA'''



def convert_dt2utc(input_datetime):
    """
    Check if the provided datetime object has timezone information.
    - If it does not have timezone information, set the timezone to UTC.
    - If it does have timezone information, convert it to UTC if it's not already in UTC.
    """
    # Check if the datetime object has timezone information
    if input_datetime.tzinfo is None or input_datetime.tzinfo.utcoffset(input_datetime) is None:
        # Set the timezone to UTC
        return input_datetime.replace(tzinfo=timezone.utc)
    else:
        # Convert the datetime to UTC
        return input_datetime.astimezone(timezone.utc)



def unix_to_datetime(unix_time_ms):
    '''Function to convert Unix timestamp (milliseconds) to a readable date'''
    return datetime.fromtimestamp(unix_time_ms / 1000, timezone.utc)







####################################################################################################
'''GEOGRAPHY'''

import cartopy.geodesic as gd
def distance_btwn_points_km(p1, p2):
    x, y, _ = gd.Geodesic().inverse(p1, p2)[0]
    return np.linalg.norm([x,y]) / 1.e3




