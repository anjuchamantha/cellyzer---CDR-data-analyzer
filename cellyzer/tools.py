import datetime
import tabulate


def print_matrix(_2dlist, headers):
    print(headers)
    print(_2dlist)
    matrix = []
    for i in range(0, len(_2dlist)):
        _2dlist[i].insert(0, headers[i])
        matrix.append(_2dlist[i])
    headers.insert(0, "")
    # print (matrix)
    # print (headers)
    print(tabulate.tabulate(matrix, headers=headers, tablefmt='pretty'))


def get_date_from_timestamp(timestamp):
    timestamp.strip()
    day, month, date, time, zone, year = timestamp.split()
    date, month, year = map(int, [date, month_string_to_number(month), year])
    hour, minute, sec = map(int, time.strip().split(":"))
    dt = datetime.datetime(year, month, date, hour, minute, sec)
    return dt


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except ValueError:
        raise ValueError('Not a month')
