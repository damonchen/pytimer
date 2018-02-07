#!/usr/bin/env python
# coding=utf-8

# author: damonchen
# date: 2018-02-07
# 给公司内部做培训，编写一个Hierarchical Timing Wheels的timer的实现


class Slot(list):
    pass


class Wheel(object):

    def __init__(self, size):
        self.size = size        # 0~59, or 0~23
        self.pointer = 0
        self._init_wheel_buffer(size)

    def _init_wheel_buffer(self, size):
        self.wheel_buffer = [Slot() for i in xrange(size)]

    def add(self, index, time, data):
        i = index % self.size
        self.wheel_buffer[i].append((time, data))


    def ticket(self):
        self.pointer = (self.pointer + 1) % self.size
        slot = self.wheel_buffer[self.pointer]
        self.wheel_buffer[self.pointer] = Slot()
        return slot

    def is_end(self):
        return (self.pointer + 1) % self.size == 0


class SecondWheel(Wheel):

    def __init__(self):
        super(SecondWheel, self).__init__(60)


class MinuteWheel(Wheel):

    def __init__(self):
        super(MinuteWheel, self).__init__(60)


class HourWheel(Wheel):

    def __init__(self):
        super(HourWheel, self).__init__(24)


class DayWheel(Wheel):

    def __init__(self):
        super(DayWheel, self).__init__(365)


class InvalidTime(StandardError):
    pass


class Time(object):

    def __init__(self, second, minute=0, hour=0, day=0):
        self.second = second
        self.minute = minute
        self.hour = hour
        self.day = day

    def __repr__(self):
        return '<time %dd-%dh-%dd-%ds>' % (self.day, self.hour, self.minute, self.second)


class WheelTimer(object):

    def __init__(self):
        self.second_wheel = SecondWheel()
        self.minute_wheel = MinuteWheel()
        self.hour_wheel = HourWheel()
        self.day_wheel = DayWheel()

    def add(self, time, data):
        if time.day > 0 and time.day < 365:
            self.day_wheel.add(time.day, time, data)
        elif time.hour > 0:
            self.hour_wheel.add(time.hour, time, data)
        elif time.minute > 0:
            self.minute_wheel.add(time.minute, time, data)
        elif time.second > 0:
            self.second_wheel.add(time.second, time, data)
        else:
            raise InvalidTime('invalid time %s', time)

    def second_ticket(self):
        if self.second_wheel.is_end():
            minute_slot = self.minute_ticket()
            for time, data in minute_slot:
                self.second_wheel.add(time.second, time, data)
        slot = self.second_wheel.ticket()
        return slot

    def minute_ticket(self):
        if self.minute_wheel.is_end():
            hour_slot = self.hour_ticket()
            for time, data in hour_slot:
                self.minute_wheel.add(time.minute, time, data)

        slot = self.minute_wheel.ticket()
        return slot

    def hour_ticket(self):
        if self.hour_wheel.is_end():
            day_slot = self.day_ticket()
            for time, data in day_slot:
                self.hour_wheel.add(time.hour, time, data)

        slot = self.hour_wheel.ticket()
        return slot

    def day_ticket(self):
        slot = self.day_wheel.ticket()
        return slot

    def ticket(self):
        slot = self.second_ticket()
        return slot
