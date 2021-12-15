from application import app
from utils import convert_date
from config import DB
from orm import ORM
from sale import Sale
from purchaser import Purchaser
from bid import Bid


def add_sale_from_form(form):
    fy, qtr, month = convert_date(form['auction'])
    volume = int(form['volume'])
    min_bid = float(form['min_bid'])
    sale_kwargs = {
        'name': form['name'].capitalize(),
        'fy': fy,
        'qtr': qtr,
        'month': month,
        'volume': volume,
        'min_bid': min_bid,
        'min_bid_mbf': min_bid / volume
    }

    sale = Sale(**sale_kwargs)
    sale.set_db(DB)
    sale.insert_self()
    sale.ref = ORM.get_last_primary(DB, Sale)

    bids = []
    for key in form:
        split = key.split('_')
        if split[0] == 'purchaser':
            number = split[2]
            if split[1] == 'name':
                if form[key] == 'new':
                    bids.append([form[f'purchaser_new_{number}'], float(form[f'purchaser_bid_{number}']), True])
                else:
                    bids.append([form[f'purchaser_name_{number}'], float(form[f'purchaser_bid_{number}']), False])
    max_bid = max([bid[1] for bid in bids])

    for bid in bids:
        if bid[2]:
            purchaser = Purchaser(name=bid[0])
            purchaser.set_db(DB)
            purchaser.insert_self()
            purchaser.ref = ORM.get_last_primary(DB, Purchaser)
        else:
            purchaser = app.config['PURCHASERS'][bid[0]]

        new_bid = Bid(sale_ref=sale.ref, purchaser_ref=purchaser.ref, bid=bid[1], win=int(bid[1] == max_bid))
        new_bid.set_db(DB)
        new_bid.insert_self()

    app.config['PURCHASERS'] = ORM.select_all_purchasers(DB)
    app.config['SALES'] = ORM.select_all_sales(DB)