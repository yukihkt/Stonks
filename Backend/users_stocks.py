from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from users import Users
from stocks import Stocks
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockSymbols import getStockSymbols
app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db = SQLAlchemy(app, session_options={'autocommit': True})

# tBank Functions
# --- Get all stocks not owned 
@app.route("/not_owned_stocks/tbank/<int:user_id>")
def get_stocks_by_not_owned_customer_id(user_id):
    user_info = Users.query.filter_by(user_id=user_id).first()
    stocksList = Stocks.query.all()
    result = []
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)
        usList = []
        for us in user_stocks['Depository']:
            
            usList.append(us['symbol'])
        for stock in stocksList:
            if stock.stock_symbol not in usList:
                # stock_symbol = stock.stock_symbol
                # price = getStockPrice(userID = user_info.user_acc_id,PIN = user_info.user_pin,symbol=stock_symbol)['Price']
                # print(price)
                stock_details = {
                    'stock_id':stock.stock_id,
                    'stock_symbol':stock.stock_symbol,
                    'stock_name':stock.stock_name,
                }
                result.append(stock_details)
                # stock.stock_price = price
                # result.append(stock)
        print(result)
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stocks for stocks in result]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404
    
# tBank Functions
#Get Stocks Owned By User In tBank via getCustomerStocks.py
@app.route("/users_stocks/tbank/<int:user_id>")
def find_by_user_id_tbank(user_id):
    user_info = Users.query.filter_by(user_id=user_id).first()
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)
        if user_stocks:
            stocks = []
            for x in user_stocks['Depository']:
                p = {
                    "customerID": x['customerID'],
                    "price": x['price'],
                    "quantity": x['quantity'],
                    "symbol": x['symbol'],
                    "company": getStockSymbols(x['symbol']),
                    "tradingDate": x['tradingDate']
                } 
                stocks.append(p)


            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "user_stocks": [
                            # users for users in user_stocks['Depository']
                            stocks
                            ]
                    }
                }
            ),200
        return jsonify(
            {
                "code": 404,
                "message": "There are no stocks for this user."
            }
        ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)