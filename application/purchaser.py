from statistics import mean, StatisticsError
from orm import ORM
from config import PURCHASER_BIDS_ATTRS, MONTHS
from utils import table_console_view


class Purchaser(ORM):
    args = {'ref': 'INTEGER',
            'name': 'TEXT'}

    exclude = ('ref', 'db', 'bids', 'num_bids', 'stats')

    primary_key = 'ref'

    foreign_key = None

    def __init__(self, ref=None, name=None):
        super().__init__(ref)
        self.name = name

        self.db = None
        self.bids = None
        self.num_bids = 0
        self.stats = None

    def get_bids(self):
        conn, cur = self.connect_db(self.db)
        sql = f"""SELECT * FROM bids WHERE purchaser_ref = ?"""
        cur.execute(sql, [self.ref])
        data = cur.fetchall()
        data = sorted(data, key=lambda x: x[3], reverse=True)

        self.bids = {}
        for z, i in enumerate(data):
            sql = f"""SELECT name, month, qtr, fy, volume, min_bid, min_bid_mbf FROM sales WHERE ref = ?"""
            cur.execute(sql, [i[1]])
            name, month, qtr, fy, volume, min_bid, min_bid_mbf = cur.fetchall()[0]

            bid = i[3]
            bid_mbf = bid / volume
            ob = bid - min_bid
            ob_mbf = bid_mbf - min_bid_mbf
            ob_pct = (ob / min_bid) * 100
            win = i[4] == 1

            self.bids[name] = {
                'month': month,
                'qtr': qtr,
                'fy': fy,
                'volume': volume,
                'min_bid': min_bid,
                'min_bid_mbf': min_bid_mbf,
                'win': win,
                'bid': bid,
                'bid_mbf': bid_mbf,
                'ob': ob,
                'ob_mbf': ob_mbf,
                'ob_pct': ob_pct
            }
        conn.close()
        self.num_bids = len(self.bids)
        #self.print_bids()

    def bids_to_table(self):
        if not self.bids:
            self.get_bids()
        head = [['Sale'] + [PURCHASER_BIDS_ATTRS[key][0] for key in PURCHASER_BIDS_ATTRS]]
        data = []
        for sale_name in self.bids:
            temp = [sale_name] + [PURCHASER_BIDS_ATTRS[key][1](self.bids[sale_name][key]) for key in PURCHASER_BIDS_ATTRS]
            data.append(temp)
        data = sorted(data, key=lambda x: (x[1], x[2], MONTHS[x[3]]), reverse=True)
        master = head + data
        return master

    def get_stats(self):
        if not self.bids:
            self.get_bids()

        conn, cur = self.connect_db(self.db)
        num_sales = len(cur.execute(f"""SELECT * FROM sales""").fetchall())
        conn.close()
        num_bids = len(self.bids)
        num_wins = len([1 for i in self.bids if self.bids[i]['win']])

        try:
            avg_win_ob = mean([self.bids[i]['ob'] for i in self.bids if self.bids[i]['win']])
            avg_win_ob_pct = mean([self.bids[i]['ob_pct'] for i in self.bids if self.bids[i]['win']])
        except StatisticsError:
            avg_win_ob = 0
            avg_win_ob_pct = 0

        self.stats = {
            'name': self.name,
            'num_bids': num_bids,
            'bids_pct': (num_bids / num_sales) * 100,
            'num_wins': num_wins,
            'win_pct': (num_wins / num_bids) * 100,
            'avg_ob': mean([self.bids[i]['ob'] for i in self.bids]),
            'avg_win_ob': avg_win_ob,
            'avg_ob_pct': mean([self.bids[i]['ob_pct'] for i in self.bids]),
            'avg_win_ob_pct': avg_win_ob_pct
        }


    def print_bids(self):
        print(f'Number of Bids: {self.num_bids}')
        for sale in self.bids:
            print(f'Sale: {sale}')
            for sub in self.bids[sale]:
                print(f'\t{sub}: {self.bids[sale][sub]}')
            print()

