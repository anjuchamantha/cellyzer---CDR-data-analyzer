import datetime
import tabulate


def get_weighted_edge_list(edge_list, directed):
    weighted_edge_list = []

    if not directed:
        # only the connections are cared.
        # return a list of lists of [user1,use2,number_of_connections]
        for edge in edge_list:
            count = edge_list.count(edge)
            reversed_edge = edge.copy()
            reversed_edge.reverse()
            r_count = edge_list.count(reversed_edge)
            weight = count + r_count
            weighted_edge = edge.copy()
            weighted_edge.append(weight)

            not_added = True
            for i in weighted_edge_list:
                if (edge == [i[0], i[1]]) or (reversed_edge == [i[0], i[1]]):
                    not_added = False
                    break
            if not_added:
                weighted_edge_list.append(weighted_edge)

        return weighted_edge_list
    if directed:
        # return a list of lists of [user1,use2,number_of_connections]
        for edge in edge_list:
            weight = edge_list.count(edge)
            weighted_edge = edge.copy()
            weighted_edge.append(weight)

            not_added = True
            for i in weighted_edge_list:
                if edge == [i[0], i[1]]:
                    not_added = False
                    break
            if not_added:
                weighted_edge_list.append(weighted_edge)

        return weighted_edge_list


def print_matrix(matrix, headers):
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
