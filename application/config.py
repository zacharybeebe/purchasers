from utils import (
    price,
    win,
    percent,
    error_check_int,
    error_check_float,
    html_date_today
)

DB = 'data/database.db'

INDEX = """This is dashboard to display Timber Sale Auction results and statistics for the South Puget Sound Region of the DNR.
<br><br>
The Timber Sale and Purchaser data starts at the acquisition of Capital Forest in June of 2014.
<br><br>
To view Timber Sale or Purchaser statistics, click on Sales or Purchasers in the top Navigation Bar. To add a newly auctioned<br>
Timber Sale to the database, click on Add Sale in the side Navigation Bar. To view graphs of the Timber Sale or Purchaser data, click<br>
on the Sale Graphs or Purchaser Graphs in the side Navigation Bar.
"""


BID_DISPLAY = ['Purchaser', 'Winner', 'Bid $', 'Bid per MBF', 'Overbid $', 'Overbid per MBF', 'Overbid %']


DISPLAY_ATTRS = {
    'volume': 'Volume',
    'min_bid': 'Min Bid',
    'min_bid_mbf': 'Min Bid per MBF',
    'qtr': 'Auction Quarter',
    'month': 'Auction Month',
    'fy': 'Auction Fiscal Year',
    'ob': 'Average Overbid',
    'ob_mbf': 'Average Overbid per MBF',
    'ob_pct': 'Average Overbid Percent'
}

LIST_ATTRS = {
    'qtr': [1, 2, 3, 4],
    'month': ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
}

PURCHASER_BIDS_ATTRS = {
    'fy': ['FY', int],
    'qtr': ['Quarter', int],
    'month': ['Month', str],
    'volume': ['MBF', int],
    'min_bid': ['Min Bid', price],
    'min_bid_mbf': ['Min Bid per MBF', price],
    'win': ['Win', win],
    'bid': ['Bid', price],
    'bid_mbf': ['Bid per MBF', price],
    'ob': ['Overbid', price],
    'ob_mbf': ['Overbid per MBF', price],
    'ob_pct': ['Overbid Percent', percent]
}

PURCHASER_STATS = {
    'name': ['Sale Name', str],
    'num_bids': ['Number of Bids', int],
    'bids_pct': ['Bid Frequency', percent],
    'num_wins': ['Number of Bids Won', int],
    'win_pct': ['Win Frequency', percent],
    'avg_ob': ['Average Overbid', price],
    'avg_win_ob': ['Average Overbid of Winning Bids', price],
    'avg_ob_pct': ['Average Overbid %', percent],
    'avg_win_ob_pct': ['Average Overbid % of Winning Bids', percent]
}

PURCHASER_GRAPHS = {
    'Total Revenue by Fiscal Year': ['totalrev', 'fy', 'None'],
    'Total Revenue by Quarter': ['totalrev', 'qtr', 'None'],
    'Total Revenue by Month': ['totalrev', 'month', 'None'],
    'Win % by Fiscal Year': ['win', 'fy', 'None'],
    'Win % by Quarter': ['win', 'qtr', 'None'],
    'Win % by Month': ['win', 'month', 'None'],
    'Avg Overbid by Fiscal Year': ['ob', 'fy', 'ob'],
    'Avg Overbid by Quarter': ['ob', 'qtr', 'ob'],
    'Avg Overbid by Month': ['ob', 'month', 'ob'],
    'Avg Overbid per MBF by Fiscal Year': ['ob', 'fy', 'ob-mbf'],
    'Avg Overbid per MBF by Quarter': ['ob', 'qtr', 'ob-mbf'],
    'Avg Overbid per MBF by Month': ['ob', 'month', 'ob-mbf'],
    'Avg Overbid % by Fiscal Year': ['ob', 'fy', 'ob-pct'],
    'Avg Overbid % by Quarter': ['ob', 'qtr', 'ob-pct'],
    'Avg Overbid % by Month': ['ob', 'month', 'ob-pct'],
    'Avg Sale Volume Bid On by Fiscal Year': ['size', 'fy', 'volume'],
    'Avg Sale Volume Bid On by Quarter': ['size', 'qtr', 'volume'],
    'Avg Sale Volume Bid On by Month': ['size', 'month', 'volume'],
    'Avg Sale Min Bid Bid On by Fiscal Year': ['size', 'fy', 'min-bid'],
    'Avg Sale Min Bid Bid On by Quarter': ['size', 'qtr', 'min-bid'],
    'Avg Sale Min Bid Bid On by Month': ['size', 'month', 'min-bid'],
    'Avg Sale Min Bid per MBF Bid On by Fiscal Year': ['size', 'fy', 'min-bid-mbf'],
    'Avg Sale Min Bid per MBF Bid On by Quarter': ['size', 'qtr', 'min-bid-mbf'],
    'Avg Sale Min Bid per MBF Bid On by Month': ['size', 'month', 'min-bid-mbf'],
}


SALE_GRAPHS = {
    'Number of Sales per Number of Bids': ['numbids', 'None', 'None', 'None'],
    'Avg Bids by Sale Volume Range': ['avgbids', 'volume', '1000', 'None'],
    'Avg Bids by Sale Min Bid Range': ['avgbids', 'min-bid', '500-000', 'None'],
    'Avg Bids by Sale Min Bid per MBF Range': ['avgbids', 'min-bid-mbf', '50', 'None'],
    'Number of Sales by Sale Volume Range': ['numrng', 'volume', '1000', 'None'],
    'Number of Sales by Sale Min Bid Range': ['numrng', 'min-bid', '500-000', 'None'],
    'Number of Sales by Sale Min Bid per MBF Range': ['numrng', 'min-bid-mbf', '50', 'None'],
    'Number of Sales by Fiscal Year': ['numtime', 'fy', 'None', 'None'],
    'Number of Sales by Quarter': ['numtime', 'qtr', 'None', 'None'],
    'Number of Sales by Month': ['numtime', 'month', 'None', 'None'],
    'Avg Overbid by Sale Volume Range': ['obrng', 'volume', '1000', 'ob'],
    'Avg Overbid by Sale Min Bid Range': ['obrng', 'min-bid', '500_000', 'ob'],
    'Avg Overbid by Sale Min Bid per MBF Range': ['obrng', 'min-bid-mbf', '50', 'ob'],
    'Avg Overbid per MBF by Sale Volume Range': ['obrng', 'volume', '1000', 'ob-mbf'],
    'Avg Overbid per MBF by Sale Min Bid Range': ['obrng', 'min-bid', '500-000', 'ob-mbf'],
    'Avg Overbid per MBF by Sale Min Bid per MBF Range': ['obrng', 'min-bid-mbf', '50', 'ob-mbf'],
    'Avg Overbid % by Sale Volume Range': ['obrng', 'volume', '1000', 'ob-pct'],
    'Avg Overbid % by Sale Min Bid Range': ['obrng', 'min-bid', '500-000', 'ob-pct'],
    'Avg Overbid % by Sale Min Bid per MBF Range': ['obrng', 'min-bid-mbf', '50', 'ob-pct'],
    'Avg Overbid by Fiscal Year': ['obtime', 'fy', 'ob', 'None'],
    'Avg Overbid by Quarter': ['obtime', 'qtr', 'ob', 'None'],
    'Avg Overbid by Month': ['obtime', 'month', 'ob', 'None'],
    'Avg Overbid per MBF by Fiscal Year': ['obtime', 'fy', 'ob-mbf', 'None'],
    'Avg Overbid per MBF by Quarter': ['obtime', 'qtr', 'ob-mbf', 'None'],
    'Avg Overbid per MBF by Month': ['obtime', 'month', 'ob-mbf', 'None'],
    'Avg Overbid % by Fiscal Year': ['obtime', 'fy', 'ob-pct', 'None'],
    'Avg Overbid % by Quarter': ['obtime', 'qtr', 'ob-pct', 'None'],
    'Avg Overbid % by Month': ['obtime', 'month', 'ob-pct', 'None'],
}


SALE_STATS = {
    'name': ['Sale', str],
    'fy': ['FY', int],
    'qtr': ['Quarter', int],
    'month': ['Month', str],
    'volume': ['MBF', int],
    'min_bid': ['Min Bid', price],
    'min_bid_mbf': ['Min Bid per MBF', price],
    'num_bids': ['Number of Bids', int],
    'p_name': ['Winning Purchaser', str],
    'bid': ['Winning Bid', price],
    'bid_mbf': ['Winning Bid per MBF', price],
    'ob': ['Overbid', price],
    'ob_mbf': ['Overbid per MBF', price],
    'ob_pct': ['Overbid %', percent]
}

SALE_OVERVIEW = {
    'name': ['Sale Name', str],
    'fy': ['Fiscal Year', int],
    'qtr': ['Quarter', int],
    'month': ['Month', str],
    'volume': ['Sale MBF', int],
    'min_bid': ['Min Bid', price],
    'min_bid_mbf': ['Min Bid per MBF', price],
    'num_bids': ['Number of Bids', int]
}

SALE_BIDS_ATTRS = {
    'win': ['Win', win],
    'bid': ['Bid', price],
    'bid_mbf': ['Bid per MBF', price],
    'ob': ['Overbid', price],
    'ob_mbf': ['Overbid per MBF', price],
    'ob_pct': ['Overbid Percent', percent]
}

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

MONTH_NUMS = {MONTHS[key]: key for key in MONTHS}

ADD_SALE = {
    'name': ['Sale Name', '', None],
    'auction': ['Auction Date', html_date_today(), None],
    'volume': ['Sale MBF', '', error_check_int],
    'min_bid': ['Minimum Bid', '', error_check_float],
}

