from math import ceil

def get_mps(row):
    hmmss_per_k = row["Allure moyenne en déplacement"]
    if len(hmmss_per_k) != 9:
        print(hmmss_per_k)
        return 0
    seconds = int(hmmss_per_k[6]) + 10*int(hmmss_per_k[5]) + 60*int(hmmss_per_k[3]) + 600*int(hmmss_per_k[2]) + 3600*int(hmmss_per_k[0])
    mps = 1000/seconds
    return mps

def get_best_mps(row):
    hmmss_per_k = row["Meilleure allure"]
    if len(hmmss_per_k) != 9:
        print(hmmss_per_k)
        return 0
    seconds = int(hmmss_per_k[6]) + 10*int(hmmss_per_k[5]) + 60*int(hmmss_per_k[3]) + 600*int(hmmss_per_k[2]) + 3600*int(hmmss_per_k[0])
    mps = 1000/seconds
    return mps


def get_seconds(hhmmssmmm):
    if hhmmssmmm[2] != ":":
        print(hhmmssmmm)
        return 0
    seconds = int(hhmmssmmm[7]) +  10*int(hhmmssmmm[6]) + 60*int(hhmmssmmm[4]) + 600*int(hhmmssmmm[3]) + 3600*int(hhmmssmmm[1]) + 36000*int(hhmmssmmm[0])
    return seconds


def min_seconds(row):
    return min([get_seconds(row["Temps de déplacement"]),get_seconds(row["Heure"])])


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


def classify_zone(row):
    avg_hr = row["avg_hr"]
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