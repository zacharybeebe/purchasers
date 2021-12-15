from statistics import mean

from orm import ORM
from purchaser import Purchaser
from utils import create_figure
from config import *


def get_purchaser_graph_title(graph, time, attr):
    for graph_title in PURCHASER_GRAPHS:
        if PURCHASER_GRAPHS[graph_title] == [graph, time, attr]:
            return graph_title, graph, time, attr


def display_purchaser_total_bought_by_time(purchaser, time, attr=None):
    if not purchaser.bids:
        purchaser.get_bids()

    bought = {}
    for sale in purchaser.bids:
        if purchaser.bids[sale]['win']:
            if purchaser.bids[sale][time] not in bought:
                bought[purchaser.bids[sale][time]] = [purchaser.bids[sale]['bid']]
            else:
                bought[purchaser.bids[sale][time]].append(purchaser.bids[sale]['bid'])
    if time == 'fy':
        buckets = ORM.get_fy_set(DB)
    else:
        buckets = [i for i in LIST_ATTRS[time]]

    bought_list = []
    for i in buckets:
        try:
            bought_list.append(sum(bought[i]))
        except KeyError:
            bought_list.append(0)

    buckets = [str(i) for i in buckets]
    text = [price(i) for i in bought_list]

    x_show = DISPLAY_ATTRS[time]
    y_show = 'Total Revenue'

    master = {
        x_show: buckets,
        y_show: bought_list,
        'text': text
    }
    return create_figure(master, x_show, y_show, purchaser=purchaser.name.upper())


def display_purchaser_win_pct_by_time(purchaser, time, attr=None):
    if not purchaser.bids:
        purchaser.get_bids()

    wins = {}
    for sale in purchaser.bids:
        if purchaser.bids[sale][time] not in wins:
            wins[purchaser.bids[sale][time]] = [purchaser.bids[sale]['win']]
        else:
            wins[purchaser.bids[sale][time]].append(purchaser.bids[sale]['win'])

    if time == 'fy':
        buckets = ORM.get_fy_set(DB)
    else:
        buckets = LIST_ATTRS[time]

    wins_list = []
    for i in buckets:
        try:
            wins_list.append(round((len([1 for j in wins[i] if j]) / len(wins[i])) * 100, 1))
        except KeyError:
            wins_list.append(0)

    buckets = [str(i) for i in buckets]

    x_show = f'Sale {DISPLAY_ATTRS[time]}'
    y_show = 'Win Percentage'

    master = {
        x_show: buckets,
        y_show: wins_list,
        'text': wins_list
    }
    return create_figure(master, x_show, y_show, purchaser=purchaser.name.upper())


def display_purchaser_ob_avg_by_time(purchaser, time, attr):
    if not purchaser.bids:
        purchaser.get_bids()

    bought = {}
    for sale in purchaser.bids:
        if purchaser.bids[sale][time] not in bought:
            bought[purchaser.bids[sale][time]] = [purchaser.bids[sale][attr]]
        else:
            bought[purchaser.bids[sale][time]].append(purchaser.bids[sale][attr])

    if time == 'fy':
        buckets = ORM.get_fy_set(DB)
    else:
        buckets = [i for i in LIST_ATTRS[time]]

    bought_list = []
    for i in buckets:
        try:
            bought_list.append(mean(bought[i]))
        except KeyError:
            bought_list.append(0)

    buckets = [str(i) for i in buckets]

    if attr == 'ob_pct':
        text = [percent(i) for i in bought_list]
    else:
        text = [price(i) for i in bought_list]

    x_show = DISPLAY_ATTRS[time]
    y_show = DISPLAY_ATTRS[attr]

    master = {
        x_show: buckets,
        y_show: bought_list,
        'text': text
    }
    return create_figure(master, x_show, y_show, purchaser=purchaser.name.upper())


def display_purchaser_avg_size_bid_by_time(purchaser, time, attr):
    if not purchaser.bids:
        purchaser.get_bids()

    bought = {}
    for sale in purchaser.bids:
        if purchaser.bids[sale][time] not in bought:
            bought[purchaser.bids[sale][time]] = [purchaser.bids[sale][attr]]
        else:
            bought[purchaser.bids[sale][time]].append(purchaser.bids[sale][attr])

    if time == 'fy':
        buckets = ORM.get_fy_set(DB)
    else:
        buckets = [i for i in LIST_ATTRS[time]]

    bought_list = []
    for i in buckets:
        try:
            bought_list.append(mean(bought[i]))
        except KeyError:
            bought_list.append(0)

    buckets = [str(i) for i in buckets]

    if attr == 'volume':
        text = [str(round(i, 0)) for i in bought_list]
    else:
        text = [price(i) for i in bought_list]

    x_show = DISPLAY_ATTRS[time]
    y_show = f'Avg Sale Size Bid On for {DISPLAY_ATTRS[attr]}'

    master = {
        x_show: buckets,
        y_show: bought_list,
        'text': text
    }
    return create_figure(master, x_show, y_show, purchaser=purchaser.name.upper())


PURCHASER_GRAPH_KEYS = {
    'win': display_purchaser_win_pct_by_time,
    'ob': display_purchaser_ob_avg_by_time,
    'totalrev': display_purchaser_total_bought_by_time,
    'size': display_purchaser_avg_size_bid_by_time
}


if __name__ == '__main__':
    p = ORM.select_by_name(DB, Purchaser, 'SPI')
    times = ['fy', 'qtr', 'month']
    attrs = ['volume', 'min_bid', 'min_bid_mbf']
    #attrs = ['ob', 'ob_mbf', 'ob_pct']
    for time in times:
        for attr in attrs:
            display_purchaser_avg_size_bid_by_time(p, time, attr)


