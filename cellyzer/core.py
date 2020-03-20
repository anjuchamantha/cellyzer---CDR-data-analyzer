"""
Main classes are modeled here

classes
---------
CallRecord
User
Message
Cell

"""

import matplotlib.pyplot as plt
import numpy as np
import math


# class DataFrame:
#     def __init__(self):


class CallRecordsDF:
    # has CallRecords list with CallRecord objects
    def __init__(self, user, other_user, direction, duration, timestamp):
        self.user = user,
        self.other_user = other_user
        self.direction = direction,
        self.duration = duration,
        self.timestamp = timestamp

    # bc>>> function to check whether 2 call records are equal


class MessagesDF:
    # has Messages list with Message objects
    def __init__(self, user, other_user, direction, length, timestamp):
        self.user = user,
        self.other_user = other_user
        self.direction = direction,
        self.length = length,
        self.timestamp = timestamp

    # bc>>> function to check whether 2 messages are equal


class CellsDF:
    # has Messages dictionary with Cell objects : key is cell_id
    def __init__(self, cell_id, latitude, longitude):
        self.cell_id = cell_id,
        self.latitude = latitude,
        self.longitude = longitude

    # bc>>> get location
    # bc>>> check 2 locations are equal


def graph():
    x = np.arange(0, math.pi * 2, 0.05)
    y = np.sin(x)
    plt.xlabel("angle")
    plt.ylabel("sine")
    plt.title("Sine Wave")
    plt.plot(x, y)
    plt.show()
    return
