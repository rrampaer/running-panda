from math import ceil


def wow():
    return(print("wow"))


def prepare_hist(s):
    if isinstance(s.max(), float):
        max_value = ceil(s.max())
    else:
        max_value = int(s.max())
    values = s.dropna().tolist()
    bins = range(max_value+1)
    return values, bins


def classify_zone(avg_hr):
    if avg_hr > 182:
        return 6
    elif avg_hr > 172:
        return 5
    elif avg_hr > 163:
        return 4
    elif avg_hr > 155:
        return 3
    elif avg_hr > 146:
        return 2
    elif avg_hr < 146:
        return 1