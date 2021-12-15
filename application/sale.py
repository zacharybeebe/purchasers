from orm import ORM
from config import BID_DISPLAY, SALE_BIDS_ATTRS


class Sale(ORM):
    args = {'ref': 'INTEGER',
            'name': 'TEXT',
            'fy': 'INTEGER',
            'qtr': 'INTEGER',
            'month': 'TEXT',
            'volume': 'INTEGER',
            'min_bid': 'REAL',
            'min_bid_mbf': 'REAL'}

    exclude = ('ref', 'db', 'bids', 'num_bids', 'stats')

    primary_key = 'ref'

    foreign_key = None

    def __init__(self, ref=None, name=None, fy=None, qtr=None, month=None, volume=0, min_bid=0, min_bid_mbf=0):
        super().__init__(ref)
        self.name = name
        self.fy = fy
        self.qtr = qtr
        self.month = month
        self.volume = volume
        self.min_bid = min_bid
        self.min_bid_mbf = min_bid_mbf

        self.db = None
        self.bids = None
        self.num_bids = 0
        self.stats = None

    def get_bids(self):
        conn, cur = self.connect_db(self.db)
        sql = f"""SELECT * FROM bids WHERE sale_ref = ?"""
        cur.execute(sql, [self.ref])
        data = cur.fetchall()
        data = sorted(data, key=lambda x: x[3], reverse=True)

        self.bids = {}
        for z, i in enumerate(data):
            sql = f"""SELECT name FROM purchasers WHERE ref = ?"""
            cur.execute(sql, [i[2]])
            name = cur.fetchone()[0]

            bid = i[3]
            bid_mbf = bid / self.volume
            ob = bid - self.min_bid
            ob_mbf = bid_mbf - self.min_bid_mbf
            ob_pct = (ob / self.min_bid) * 100

            self.bids[name] = {
                'win': z == 0,
                'bid': i[3],
                'bid_mbf': i[3] / self.volume,
                'ob': ob,
                'ob_mbf': ob_mbf,
                'ob_pct': ob_pct
            }
        conn.close()
        self.num_bids = len(self.bids)

    def get_stats(self):
        if not self.bids:
            self.get_bids()
        self.stats = {
            'name': self.name,
            'fy': self.fy,
            'qtr': self.qtr,
            'month': self.month,
            'volume': self.volume,
            'min_bid': self.min_bid,
            'min_bid_mbf': self.min_bid_mbf,
            'num_bids': len(self.bids)
        }
        add_ons = ['bid', 'bid_mbf', 'ob', 'ob_mbf', 'ob_pct']
        for purchaser in self.bids:
            if self.bids[purchaser]['win']:
                self.stats.update({'p_name': purchaser})
                self.stats.update({key: self.bids[purchaser][key] for key in add_ons})
                break

    def bids_to_table(self):
        if not self.bids:
            self.get_bids()
        head = [['Purchaser'] + [SALE_BIDS_ATTRS[key][0] for key in SALE_BIDS_ATTRS]]
        data = []

        bids_sorted = sorted([key for key in self.bids], key=lambda x: self.bids[x]['bid'], reverse=True)
        for sale_name in bids_sorted:
            temp = [sale_name] + [SALE_BIDS_ATTRS[key][1](self.bids[sale_name][key]) for key in SALE_BIDS_ATTRS]
            data.append(temp)
        master = head + data

        return master









