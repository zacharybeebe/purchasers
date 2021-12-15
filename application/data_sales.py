from statistics import mean

from orm import ORM
from sale import Sale
from purchaser import Purchaser
from bid import Bid
from utils import create_figure
from config import *


def get_sale_graph_title(graph, arg1, arg2, arg3):
    for graph_title in SALE_GRAPHS:
        if SALE_GRAPHS[graph_title] == [graph, arg1, arg2, arg3]:
            return graph_title, graph, arg1, arg2, arg3


def sales_by_attr(attr, rng=False, step=0):
    sales = ORM.select_all_sales(DB)
    attr_sales = {}

    if not rng:
        for sale_name in sales:
            sale = sales[sale_name]
            if sale[attr] not in attr_sales:
                attr_sales[sale[attr]] = [sale]
            else:
                attr_sales[sale[attr]].append(sale)
    else:
        for sale_name in sales:
            sale = sales[sale_name]
            val = (sale[attr] // step) * step
            if val not in attr_sales:
                attr_sales[val] = [sale]
            else:
                attr_sales[val].append(sale)
    return attr_sales


def display_num_sales_by_num_bids(other1=None, other2=None, other3=None):
    sales = sales_by_attr('num_bids')
    num_bids = sorted(sales)
    num_sales = [len(sales[i]) for i in num_bids]

    x_show = 'Number of Bids'
    y_show = 'Number of Sales'

    master = {
        x_show: num_bids,
        y_show: num_sales,
        'text': num_sales
    }
    return create_figure(master, x_show, y_show)


def display_avg_bids_by_rng(rng, step, attr=None):
    step = int(step)
    sales = sales_by_attr(rng, rng=True, step=step)
    ranges = sorted(list(sales))

    avg_ob = []
    for i in ranges:
        obs = []
        for sale in sales[int(i)]:
            obs.append(len(sale.bids))
        avg_ob.append(round(mean(obs), 2))

    text = [price(i, add_dollar_sign=False) for i in avg_ob]

    if rng == 'volume':
        ranges = [f'{i} - {i + (step - 1)}' for i in ranges]
    else:
        ranges = [f'{price(i)} - {price(i + (step - 1), add_dollar_sign=False)}' for i in ranges]

    x_show = f'Sale {DISPLAY_ATTRS[rng]} Range'
    y_show = 'Average Number of Bids'

    master = {
        x_show: ranges,
        y_show: avg_ob,
        'text': text
    }
    return create_figure(master, x_show, y_show)


def display_num_sales_by_range(rng, step, attr=None):
    step = int(step)
    sales = sales_by_attr(rng, rng=True, step=step)
    ranges = sorted(list(sales))
    num_sales = [len(sales[i]) for i in ranges]

    if rng == 'volume':
        ranges = [f'{i} - {i + (step - 1)}' for i in ranges]
    else:
        ranges = [f'{price(i)} - {price(i + (step - 1), add_dollar_sign=False)}' for i in ranges]

    x_show = f'Sale {DISPLAY_ATTRS[rng]} Range'
    y_show = 'Number of Sales'

    master = {
        x_show: ranges,
        y_show: num_sales,
        'text': num_sales
    }
    return create_figure(master, x_show, y_show)


def display_num_sales_by_time(time, other1=None, other2=None):
    sales = sales_by_attr(time)
    if time == 'fy':
        buckets = ORM.get_fy_set(DB)
    else:
        buckets = LIST_ATTRS[time]

    num_sales = [len(sales[i]) for i in buckets]

    buckets = [str(i) for i in buckets]
    x_show = f'Sale {DISPLAY_ATTRS[time]}'
    y_show = 'Number of Sales'

    master = {
        x_show: buckets,
        y_show: num_sales,
        'text': num_sales
    }
    return create_figure(master, x_show, y_show)


def display_avg_ob_by_range(rng, step, attr):
    step = int(step)
    sales = sales_by_attr(rng, rng=True, step=step)
    ranges = sorted(list(sales))

    avg_ob = []
    for i in ranges:
        obs = []
        for sale in sales[int(i)]:
            for bid in sale.bids:
                if sale.bids[bid]['win']:
                    obs.append(sale.bids[bid][attr])
                    break
        avg_ob.append(round(mean(obs), 1))

    if attr == 'ob_pct':
        text = [percent(i) for i in avg_ob]
    else:
        text = [price(i) for i in avg_ob]

    if rng == 'volume':
        ranges = [f'{i} - {i + (step - 1)}' for i in ranges]
    else:
        ranges = [f'{price(i)} - {price(i + (step - 1), add_dollar_sign=False)}' for i in ranges]

    x_show = f'Sale {DISPLAY_ATTRS[rng]} Range'
    y_show = DISPLAY_ATTRS[attr]

    master = {
        x_show: ranges,
        y_show: avg_ob,
        'text': text
    }
    return create_figure(master, x_show, y_show)


def display_avg_ob_by_time(time, attr, other=None):
    sales = sales_by_attr(time)
    if time == 'fy':
        buckets = sorted(list(sales))
    else:
        buckets = LIST_ATTRS[time]

    avg_ob = []
    for i in buckets:
        obs = []
        for sale in sales[i]:
            for bid in sale.bids:
                if sale.bids[bid]['win']:
                    obs.append(sale.bids[bid][attr])
                    break
        avg_ob.append(round(mean(obs), 1))

    if attr == 'ob_pct':
        text = [percent(i) for i in avg_ob]
    else:
        text = [price(i) for i in avg_ob]

    buckets = [str(i) for i in buckets]
    x_show = f'Sale {DISPLAY_ATTRS[time]}'
    y_show = DISPLAY_ATTRS[attr]

    master = {
        x_show: buckets,
        y_show: avg_ob,
        'text': text
    }
    return create_figure(master, x_show, y_show)


SALE_GRAPH_KEYS = {
    'numbids': display_num_sales_by_num_bids,
    'avgbids': display_avg_bids_by_rng,
    'numrng': display_num_sales_by_range,
    'numtime': display_num_sales_by_time,
    'obrng': display_avg_ob_by_range,
    'obtime': display_avg_ob_by_time
}


if __name__ == '__main__':
    print(int('500_000'))
    pass







