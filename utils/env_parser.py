def convert_to_bytes(size_str):
    size_str = size_str.replace(" ", "")

    if len(size_str) < 2:
        raise ValueError(f"Invalid format for size string: {size_str}")

    size, unit = size_str[:-2], size_str[-2:]

    try:
        size = int(size)
    except ValueError:
        raise ValueError(f"Invalid number in size string: {size}")

    unit = unit.upper()

    if unit == "KB":
        return size * 1024
    elif unit == "MB":
        return size * 1024**2
    elif unit == "GB":
        return size * 1024**3
    elif unit == "TB":
        return size * 1024**4
    else:
        raise ValueError(f"Invalid size unit: {unit}")


def convert_to_seconds(time_str):
    parts = time_str.split()

    if len(parts) != 2:
        raise ValueError(f"Invalid format for time string: {time_str}")

    value, unit = parts

    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"Invalid number in time string: {value}")

    unit = unit.lower()
    if unit in {"second", "seconds"}:
        seconds = value
    elif unit in {"minute", "minutes"}:
        seconds = value * 60
    elif unit in {"hour", "hours"}:
        seconds = value * 60 * 60
    elif unit in {"day", "days"}:
        seconds = value * 24 * 60 * 60
    elif unit in {"week", "weeks"}:
        seconds = value * 7 * 24 * 60 * 60
    elif unit in {"month", "months"}:
        seconds = value * 30 * 24 * 60 * 60
    else:
        raise ValueError(f"Invalid time unit in string: {unit}")

    return seconds


def convert_to_days(time_str):
    time_str = time_str.strip()  # Remove leading/trailing whitespace
    parts = time_str.split()

    if len(parts) != 2:
        raise ValueError(f"Invalid format for time string: {time_str}")

    value, unit = parts
    unit = unit.lower()

    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"Invalid number in time string: {value}")

    conversion_dict = {
        "day": 1,
        "days": 1,
        "month": 30,
        "months": 30,
        "year": 365,
        "years": 365,
    }

    if unit not in conversion_dict:
        raise ValueError(f"Invalid time unit in string: {unit}")

    return value * conversion_dict[unit]


if __name__ == "__main__":
    print(convert_to_days("100 days"))
    print(type(convert_to_days("100 days")))
