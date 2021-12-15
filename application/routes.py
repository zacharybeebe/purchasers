from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session
)
from application import app
from config import (
    INDEX,
    SALE_OVERVIEW,
    SALE_STATS,
    SALE_GRAPHS,
    PURCHASER_STATS,
    PURCHASER_GRAPHS,
    ADD_SALE
)
from utils import (
    check_two_words,
    correct_attr
)
from routes_funcs import add_sale_from_form
from data_purchasers import (
    get_purchaser_graph_title,
    PURCHASER_GRAPH_KEYS
)
from data_sales import (
    get_sale_graph_title,
    SALE_GRAPH_KEYS
)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', index_prompt=INDEX)


@app.route('/purchaser_graphs_<purchaser_name>_<graph>_<time>_<attr>')
def purchaser_graphs(purchaser_name, graph, time, attr):
    purchaser_name = check_two_words(purchaser_name)
    fig = 'None'
    graph_values = ['None', 'None', 'None', 'None']
    if purchaser_name != 'None':
        p = app.config['PURCHASERS'][purchaser_name]
        fig = PURCHASER_GRAPH_KEYS[graph](p, time, correct_attr(attr))
        graph_values = get_purchaser_graph_title(graph, time, attr)
    return render_template('purchaser_graphs.html', purchasers=app.config["PURCHASERS"], buttons=PURCHASER_GRAPHS, fig=fig,
                           purchaser_name=purchaser_name, graph_values=graph_values)


@app.route('/sale_graphs_<graph>_<arg1>_<arg2>_<arg3>')
def sale_graphs(graph, arg1, arg2, arg3):
    fig = 'None'
    graph_values = ['None', 'None', 'None', 'None', 'None']
    if graph != 'None':
        args = [correct_attr(i) for i in [arg1, arg2, arg3]]
        fig = SALE_GRAPH_KEYS[graph](*args)
        graph_values = get_sale_graph_title(graph, arg1, arg2, arg3)
    return render_template('sale_graphs.html', buttons=SALE_GRAPHS, fig=fig, graph_values=graph_values)


@app.route('/purchasers')
def purchasers():
    table = [[PURCHASER_STATS[key][0] for key in PURCHASER_STATS]]
    for purchaser_name in app.config['PURCHASERS']:
        p = app.config['PURCHASERS'][purchaser_name]
        table.append([PURCHASER_STATS[key][1](p.stats[key]) for key in PURCHASER_STATS])
    return render_template('purchasers.html', table=table)


@app.route('/purchaser_<purchaser_name>')
def purchaser(purchaser_name):
    p = app.config['PURCHASERS'][purchaser_name]
    table = p.bids_to_table()
    return render_template('purchaser.html', purchaser=p, table=table, buttons=PURCHASER_GRAPHS)


@app.route('/sales')
def sales():
    table = [[SALE_STATS[key][0] for key in SALE_STATS]]
    for sale_name in app.config['SALES']:
        sale = app.config['SALES'][sale_name]
        table.append([SALE_STATS[key][1](sale.stats[key]) for key in SALE_STATS])
    return render_template('sales.html', table=table)


@app.route('/sale_<sale_name>')
def sale(sale_name):
    sale = app.config['SALES'][sale_name]
    bid_table = sale.bids_to_table()
    return render_template('sale.html', sale=sale, bid_table=bid_table, sale_overview=SALE_OVERVIEW)


@app.route('/add_sale', methods=['POST', 'GET'])
def add_sale():
    purchasers_list = [key for key in app.config["PURCHASERS"]]
    if request.method == 'POST':
        add_sale_from_form(request.form)
        return redirect(url_for('sales'))
    return render_template('add_sale.html', add_sale_form=ADD_SALE, purchasers=purchasers_list)











