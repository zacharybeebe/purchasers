from datetime import date
from json import dumps
from plotly.express import bar
from plotly.utils import PlotlyJSONEncoder

MONTH_NUMS = {
    1: ['January', 3, False],
    2: ['February', 3, False],
    3: ['March', 3, False],
    4: ['April', 4, False],
    5: ['May', 4, False],
    6: ['June', 4, False],
    7: ['July', 1, True],
    8: ['August', 1, True],
    9: ['September', 1, True],
    10: ['October', 2, True],
    11: ['November', 2, True],
    12: ['December', 2, True]
}


def create_figure(data, x, y, purchaser=None, show_figure=False):
    if purchaser:
        title = f'{purchaser} {y} per {x}'
    else:
        title = f'{y} per {x}'
    fig = bar(data, x=x, y=y, text='text', title=title)
    fig.update_traces(textangle=0)

    if show_figure:
        fig.show()

    fig_json = dumps(fig, cls=PlotlyJSONEncoder)
    return fig_json


def table_console_view(table):
    if type(table) in [list, dict]:
        space = 20
        display = []

        if isinstance(table, list):
            for row in table:
                temp = []
                for i in row:
                    if isinstance(i, float):
                        val = str(round(i, 1))
                    else:
                        val = str(i)
                    temp.append(f"""{val}{' ' * (space - len(val))}""")
                display.append(''.join(temp))
        else:
            header = list(table.keys())
            temp = [[f"""{i}{' ' * (space - len(str(i)))}""" for i in header]]
            for i in range(len(table[header[0]])):
                add = []
                for head in header:
                    if isinstance(table[head][i], float):
                        val = str(round(table[head][i], 1))
                    else:
                        val = str(table[head][i])
                    add.append(f"""{val}{' ' * (space - len(val))}""")
                temp.append(add)
            for row in temp:
                display.append(''.join(row))
        return display
    else:
        raise Exception(f'Incorrect data type: {type(table)}, need "list" or "dict"')


def win(value):
    if value == 0:
        return 'No'
    else:
        return 'Yes'


def percent(value):
    return f'{round(value, 1)}%'


def price(value, add_dollar_sign=True):
    val_list = [i for i in str(round(value, 2))]
    if '.' not in val_list:
        add_to = ['.', '0', '0']
        for i in add_to:
            val_list.append(i)
    else:
        if len(val_list[-(len(val_list) - val_list.index('.')):]) < 3:
            val_list.append('0')
    temp = [i for i in reversed(val_list)]
    added = 0
    for i in range(3, len(val_list)):
        if i != 3 and i % 3 == 0:
            temp.insert(i + added, ',')
            added += 1
    if add_dollar_sign:
        return f"""${''.join([i for i in reversed(temp)])}"""
    else:
        return f"""{''.join([i for i in reversed(temp)])}"""


def error_check_int(value):
    try:
        x = int(value)
        return True
    except ValueError:
        return False


def error_check_float(value):
    try:
        x = float(value)
        return True
    except ValueError:
        return False


def convert_date(date):
    year, month, day = [int(i) for i in date.split('-')]
    month_name, qtr = MONTH_NUMS[month][0], MONTH_NUMS[month][1]
    if MONTH_NUMS[month][2]:
        fy = year + 1
    else:
        fy = year
    return fy, qtr, month_name


def html_date_today():
    dt = date.today()
    y = dt.year
    m = f"""{'0' * (2 - len(str(dt.month)))}{dt.month}"""
    d = f"""{'0' * (2 - len(str(dt.day)))}{dt.day}"""
    return f'{y}-{m}-{d}'


def correct_attr(attr):
    if '-' in attr:
        return attr.replace('-', '_')
    else:
        return attr


def check_two_words(value):
    if '_' in value:
        return value.replace('_', ' ')
    else:
        return value





if __name__ == '__main__':
    print(convert_date('11-27-2030'))
    print(convert_date('01-22-2031'))
    print(html_date_today())

