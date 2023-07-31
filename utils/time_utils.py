import datetime, math


def convert_raw_expired_time_to_sec(utc_expire_time: datetime) -> int:
    if type(utc_expire_time) is int and utc_expire_time > 0:
        return utc_expire_time
    expire_time = int(
        utc_expire_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )
    return expire_time


def convert_seconds_to_days(seconds):
    seconds_in_a_day = 60 * 60 * 24  # 86400
    days = math.ceil(seconds / seconds_in_a_day)
    return days


if __name__ == "__main__":
    utc_expire_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    print(convert_raw_expired_time_to_sec(datetime.datetime.utcnow()), "seconds")
