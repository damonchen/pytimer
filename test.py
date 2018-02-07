from timer import Time, WheelTimer


class Data(object):

    def __init__(self, v):
        self.v = v

    def __call__(self):
        print(self.v)

    def __repr__(self):
        return self.v


wheel_timer = WheelTimer()

wheel_timer.add(Time(10), Data("value for test"))
wheel_timer.add(Time(1, 1), Data("value for test2"))
# 3600 + 61 = 3661 -> 3660 will print value for test3
wheel_timer.add(Time(1, minute=1, hour=1), Data("value for test3"))
# 86400 + 3660 = 90060
wheel_timer.add(Time(1, minute=1, hour=1, day=1), Data("value for test3"))


index = 0
while True:
    # print('index: %s' % index)
    slot = wheel_timer.ticket()
    if index in [9, 60, 3660, 90060]:
        print(index, len(slot) > 0)

    index += 1

    if index > 100000:
        break

