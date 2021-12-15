from flask import Flask
from config import DB
from orm import ORM
from sale import Sale
from purchaser import Purchaser
from bid import Bid

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisIsSupposedToBeSecret"

app.config['PURCHASERS'] = ORM.select_all_purchasers(DB)
app.config['SALES'] = ORM.select_all_sales(DB)


from application import routes