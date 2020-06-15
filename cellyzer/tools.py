import datetime
import tabulate
import logging
import sys
import webbrowser

from . import matrix as matrixFile


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
    print('matrix : ', matrix)
    print('header : ', headers)
    if len(matrix) > 10:
        print("Matrix Length : ", len(matrix))
        html = """
        <html>
        <body>
            <h1>Connection Matrix</h1>
            <br>
            {table}
        </body>
        </html>
        """
        table = tabulate.tabulate(matrix, headers=headers, tablefmt='html', stralign='center')
        print('table : ', table)
        b = table.encode('utf-8')
        f = open('connection_matrix.html', 'wb')
        f.write(b)
        f.close()
        webbrowser.open_new_tab('connection_matrix.html')
    else:
        print(">> connection matrix")
        print(tabulate.tabulate(matrix, headers=headers, tablefmt='pretty'))


def print_matrix_new(matrix, headers):
    if len(matrix) > 0:
        print("Matrix Length : ", len(matrix))
        html_tag = matrixFile.matrix_html_head
        table_header = create_header(headers)
        table_body = create_rows(matrix)
        html_tag += '<table> \n {} \n {} \n </table>  \n </body> \n</html>'.format(table_header, table_body)
        f = open('outputs\\connection_matrix.html', 'w')
        f.write(html_tag)
        f.close()
        webbrowser.open_new_tab('outputs\\connection_matrix.html')


def create_rows(matrix, text_align='center'):
    row_tag_list = '<tbody>'
    for each_row in matrix:
        if each_row[0] != '':
            each_row_tag = '<tr>'
            for each_row_item in each_row:
                if each_row_item == each_row[0]:
                    each_row_items = '<td style="text-align: {};" id="main-row"> {} </td>'.format(text_align, each_row_item)
                else:
                    each_row_items = '<td style="text-align: {};"> {} </td>'.format(text_align, each_row_item)
                each_row_tag += each_row_items
            each_row_tag_end = each_row_tag + '</tr> \n'
            row_tag_list += each_row_tag_end
    row_tag_list_end = row_tag_list + '</tbody>'
    return row_tag_list_end


def create_header(headers, text_align='center'):
    new_tag = '<thead> \n <tr>'
    for each_header in headers:
        tag = '<th style="text-align: {};" id="main-column"> {} </th>'.format(text_align, each_header)
        new_tag += tag
    tag_end = new_tag + '</tr> \n </thead>'
    return tag_end


def get_datetime_from_timestamp(timestamp):
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


def get_index_of_day(string):
    d = {
        'Mon': 1,
        'Tue': 2,
        'Wed': 3,
        'Thu': 4,
        'Fri': 5,
        'Sat': 6,
        'Sun': 7
    }
    day = string.split()[0]
    try:
        out = d[day]
        return out
    except ValueError:
        raise ValueError('Not a day')
