from datetime import datetime, timedelta

class FakeTime:
    _fake_time = datetime(2014, 12, 11, 18, 00)

    @classmethod
    def now(cls):
        return cls._fake_time

    @classmethod
    def advance(cls, seconds=0, minutes=0, hours=0):
        cls._fake_time += timedelta(seconds=seconds, minutes=minutes, hours=hours)
        return cls._fake_time

    @classmethod
    def reset(cls):
        cls._fake_time = datetime.now()
        return cls._fake_time
