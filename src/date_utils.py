# from datetime import date
from datetime import datetime, timedelta

# from https://allinpython.com/calculate-age-from-date-of-birth-in-python/

DAY_MAP_FR = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}
DAY_EN_FR_MAP = {'Monday': 'Lundi', "Tuesday": 'Mardi', "Wednesday": 'Mercredi',
                 "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"}
MONTH_MAP_FR = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet",
                8: "Aout", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
MONTH_MAP_SHORT_FR = {1: "Jan", 2: "Fév", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet",
                      8: "Aout", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc"}
MONTH_MAP_EN = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
# jour feries
HOLIDAYS = [(21, 2, 2023), (22, 2, 2023), (7, 4, 2023), (10, 4, 2023), (1, 5, 2023), (8, 5, 2023),
            (18, 5, 2023), (22, 5, 2023), (29, 5, 2023), (14, 7, 2023), (15, 8, 2023),
            (1, 11, 2023), (2, 11, 2023), (25, 12, 2023), (1, 1, 2024), (13, 2, 2024), (14, 2, 2024),
            (29, 3, 2024), (1, 4, 2024), (1, 5, 2024),
            (8, 5, 2024), (9, 5, 2024), (20, 5, 2024), (22, 5, 2024), (14, 7, 2024), (15, 8, 2024), (1, 11, 2024),
            (11, 11, 2024), (25, 12, 2024)]


def calculate_age(birth_date, current_date):
    """
    Using birth_date, it returns the age at the current_date
    :param birth_date: (datetime)
    :param current_date: (datetime)
    :return: yers, months and days (int, int, int)
    """
    # Calculation
    years = current_date.year - birth_date.year
    months = current_date.month - birth_date.month
    days = current_date.day - birth_date.day

    # Adjust for negative differences
    if days < 0:
        months -= 1
        days += get_days_in_month(birth_date.month, birth_date.year)
    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def get_days_in_month(month, year):
    """
    Returns the number of days in a given month and year
    :param month:  (int) from 1 to 12
    :param year:  (int)
    :return:
    """
    if month == 2:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29  # Leap year
        else:
            return 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        return 30
    else:
        return 31


def duration_bw_dates(later_date, early_date):
    """
    Return duration bw dates in hours and minutes
    :param later_date:
    :param early_date:
    :return: int, float and int representing number of hours, number of precise hours, number of minutes that complete
    the hours in integer
    """
    duration = later_date - early_date
    duration_in_s = duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]
    minutes = divmod(duration_in_s, 60)[0]
    hours_float = hours + ((minutes % 60) / 60)
    return hours, hours_float, minutes


def seconds_bw_dates(later_date, early_date):
    """

    :param later_date:
    :param early_date:
    :return: durée en secondes
    """
    duration = later_date - early_date
    duration_in_s = duration.total_seconds()
    return duration_in_s


def from_dmy_to_date(dmy):
    """
    Take a date in format (day, month, year) and return a datetime object
    :param dmy: tuple (int, int, int)
    :return:
    """
    return datetime.strptime(str(dmy), "(%d, %m, %Y)")


def is_dmy_bw_dmys(main_dmy, first_dmy, last_dmy):
    """
    Return True if main_dmy is situated between first_dmy and last_dmy
    :param main_dmy: tuple in the format of dmy (day, month, year) (int, int, int)
    :param first_dmy:
    :param last_dmy:
    :return:
    """
    main_date = from_dmy_to_date(main_dmy)
    first_date = from_dmy_to_date(first_dmy)
    last_date = from_dmy_to_date(last_dmy)
    return first_date <= main_date <= last_date


def is_school_time(date_to_use, ecole_primaire=False, school_day=False):
    """
    return true if it is school_time
    :param date_to_use: datetime
    :param ecole_primaire:
    :param school_day: if True we want to know if there is school that day, otherwise we look at the exact time
    :return:
    """
    date_dmy = (date_to_use.day, date_to_use.month, date_to_use.year)

    vacations_dates = dict()
    vacations_dates["carnaval_23"] = ((11, 2, 2023), (26, 2, 2023))
    vacations_dates["paques_23"] = ((1, 4, 2023), (16, 4, 2023))
    vacations_dates["pont_mai_23"] = ((18, 5, 2023), (22, 5, 2023))
    vacations_dates["ete_23"] = ((8, 7, 2023), (31, 8, 2023))
    vacations_dates["toussaint_23"] = ((21, 10, 2023), (6, 11, 2023))
    vacations_dates["noel_23"] = ((23, 12, 2023), (8, 1, 2024))
    vacations_dates["carnaval_24"] = ((10, 2, 2024), (26, 2, 2024))
    vacations_dates["paques_24"] = ((23, 3, 2024), (8, 4, 2024))
    vacations_dates["ete_24"] = ((6, 7, 2024), (2, 9, 2024))

    for vacation_name, vacations_date in vacations_dates.items():
        first_day_vac = vacations_date[0]
        last_day_vac = vacations_date[1]
        if is_dmy_bw_dmys(main_dmy=date_dmy, first_dmy=first_day_vac, last_dmy=last_day_vac):
            return False

    # jours feries
    if date_dmy in HOLIDAYS:
        return False

    week_day = date_to_use.weekday()
    # week_day
    # day_map = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}
    if week_day in [5, 6]:
        return False
    if ecole_primaire and week_day == 2:
        return False

    if school_day:
        return True

    hour = date_to_use.hour

    if week_day in [0, 1, 3, 4]:
        if 8 <= hour < 16:
            return True
        return False

    if week_day == 2:
        if 8 <= hour < 12:
            return True
        return False

    return False


def spliting_day_night_entries(entries, entries_by_day, day_hour_start=7, night_hour_start=17, verbose=True):
    """
    Split a list of entries bw day and night shift
    :param entries: entries of a giving day, the entries of the night of following day will be added
    :return:
    """
    entries_day_shift = []
    entries_night_shift = []
    for entry in entries:
        if entry.arrival_date.hour in range(day_hour_start, night_hour_start):
            entries_day_shift.append(entry)
        if entry.arrival_date.hour >= night_hour_start:
            entries_night_shift.append(entry)

    # Then we add the entries of the night the following day
    next_day_datetime = entries[0].arrival_date + timedelta(days=1)
    next_day_dmy = (next_day_datetime.day, next_day_datetime.month, next_day_datetime.year)
    if next_day_dmy in entries_by_day:
        entries_next_day = entries_by_day[next_day_dmy]
        for entry in entries_next_day:
            if entry.arrival_date.hour < 7:
                entries_night_shift.append(entry)
    elif verbose:
        print(f"In plot_day_entries(), {next_day_dmy} not in entries_by_day")

    return entries_day_shift, entries_night_shift


def consultation_date_as_string(entry):
    if hasattr(entry, "arrival_date"):
        arrival_date = entry.arrival_date
    else:
        arrival_date = entry.arrival_date_er
    english_day = arrival_date.strftime("%A")
    french_day = DAY_EN_FR_MAP[english_day]

    date_str = f"{french_day} {arrival_date.day} {MONTH_MAP_FR[arrival_date.month]} {arrival_date.year}"
    result = f"L'enfant consulte le {date_str}.\n"
    return result
