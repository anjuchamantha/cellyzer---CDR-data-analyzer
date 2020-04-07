import datetime
import tabulate
import logging
import sys


class _AnsiColorizer(object):
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        if not stream.isatty():
            return False  # auto color only on TTYs
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                # guess false in case of error
                return False

    def write(self, text, color):
        """
        Write the given text to the stream in the given color.
        """
        color = self._colors[color]
        self.stream.write('\x1b[{}m{}\x1b[0m'.format(color, text))


class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stderr):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):
        msg_colors = {
            logging.DEBUG: ("Debug", "green"),
            logging.INFO: ("Info", "blue"),
            logging.WARNING: ("Warning", "yellow"),
            logging.ERROR: ("Error", "red")
        }

        header, color = msg_colors.get(record.levelno, "blue")
        if 'prefix' in record.__dict__:
            header = record.prefix
        else:
            header = header + ':'
        self.stream.write("{} {}\n".format(header, record.msg), color)


def print_matrix(_2dlist, headers):
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
