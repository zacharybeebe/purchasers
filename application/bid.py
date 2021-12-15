from orm import ORM


class Bid(ORM):
    args = {'ref': 'INTEGER',
            'sale_ref': 'INTEGER',
            'purchaser_ref': 'INTEGER',
            'bid': 'REAL',
            'win': 'INTEGER'}

    exclude = ('ref', 'db')

    primary_key = 'ref'

    foreign_key = [['sale_ref', 'sales', 'ref'],
                   ['purchaser_ref', 'purchasers', 'ref']]

    def __init__(self, ref=None, sale_ref=None, purchaser_ref=None, bid=0, win=0):
        super().__init__(ref)
        self.sale_ref = sale_ref
        self.purchaser_ref = purchaser_ref
        self.bid = bid
        self.win = win

        self.db = None