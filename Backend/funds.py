from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append("../")
from stocks import Stocks
from funds_users_stocks import FundsUsersStocks
from users_stocks import UsersStocks
from users_funds import UsersFunds

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Funds(db.Model):
    __tablename__ = 'funds'

    fund_id = db.Column(db.String(24), primary_key=True)
    fund_name = db.Column(db.String(64), nullable=False)
    fund_goals = db.Column(db.Float(precision=2),nullable=False)
    fund_investment_amount = db.Column(db.Float(precision=2),nullable=False)

    def __init__(self, fund_id, fund_name, fund_goals, fund_investment_amount):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.fund_goals = fund_goals
        self.fund_investment_amount = fund_investment_amount

    def json(self):
        return {"fund_id": self.fund_id, "fund_name": self.fund_name, "fund_goals": self.fund_goals, "fund_investment_amount": self.fund_investment_amount}

#--Get all Funds--#
@app.route("/funds")
def get_all():
    fundsList = Funds.query.all()
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "funds": [fund.json() for fund in fundsList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no funds."
        }
    ), 404

#-- Get a Fund --#
@app.route("/funds/<int:fund_id>")
def find_by_fund_id(fund_id):
    fund = Funds.query.filter_by(fund_id=fund_id).first()
    if fund:
        return jsonify(
            {
                "code": 200,
                "data": fund.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund not found."
        }
    ), 404

## -- Add a Fund --##
@app.route("/funds/add", methods=['POST'])
def create_fund():
    data = request.get_json()
    fund = Funds(**data)

    try:
        db.session.add(fund)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fund.fund_id
                },
                "message": "An error occurred while creating the fund."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fund.json()
        }
    ), 201

## Get Stocks by Fund ID ##
@app.route("/funds/fund_settlement/<int:fund_id>")
def get_stocks_by_fund_id(fund_id):
    fundsSettlementStockList = db.session.query(FundsUsersStocks.fund_id)\
        .filter(FundsUsersStocks.fund_id == fund_id)\
        .join(UsersStocks, FundsUsersStocks.user_stock_id == UsersStocks.user_stock_id)\
        .add_columns(UsersStocks.volume)\
        .join(Stocks, UsersStocks.stock_id == Stocks.stock_id)\
        .add_columns(Stocks.stock_name)\
        .all()
    
    if len(fundsSettlementStockList):
        print("------------------------------" + str(fundsSettlementStockList[0]))
        return jsonify(
            {
                "code": 200,
                "data":[
                    {
                        "fund_id":fundSettlement[0], 
                        "volume":fundSettlement[1], 
                        "stock_name":fundSettlement[2]
                    } for fundSettlement in fundsSettlementStockList
                ]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund stocks not found."
        }
    ), 404

## Get Funds by User ID ##
@app.route("/funds/user_funds/<int:user_id>")
def get_funds_by_user_id(user_id):
    fundsList = db.session.query(UsersFunds.fund_id)\
        .filter(UsersFunds.user_id == user_id)\
        .join(Funds, UsersFunds.fund_id == Funds.fund_id)\
        .add_columns(Funds.fund_name)\
        .add_columns(Funds.fund_goals)\
        .add_columns(Funds.fund_investment_amount)\
        .all()
    
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data":[
                    {
                        "fund_id":fund[0], 
                        "fund_name":fund[1],
                        "fund_goals":fund[2],
                        "fund_investment_amount":fund[3],
                        
                    } for fund in fundsList
                ]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "User funds not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)