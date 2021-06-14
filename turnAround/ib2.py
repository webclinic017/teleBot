from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time


class IBapi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

app = IBapi()

def run_loop():
    app.run()

def FX_order(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    return contract

def starHere(tick, buy, take, stop):
    app.connect('127.0.0.1', 7497, 123)
    app.nextorderId = None

# Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

# Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            print('connected')
            print()
            break
        else:
            print('waiting for connection')
            time.sleep(1)

# Create order object
    parent = Order()
    parent.tif = "DAY"
    parent.OutsideRth = True # выполнять вне сессии
    parent.ConditionsIgnoreRth = True  # выполнять вне сессии
    parent.action = 'BUY'
    parent.totalQuantity = 5
    parent.orderType = 'LMT'
    parent.lmtPrice = buy
    parent.orderId = app.nextorderId
    app.nextorderId += 1
    parent.transmit = False

# Create stop loss order object
    stop_order = Order()
    stop_order.tif = "GTC"
    stop_order.action = "SELL" if parent.action == "BUY" else "BUY"
    stop_order.totalQuantity = 5
    stop_order.orderType = 'STP'
    stop_order.auxPrice = stop
    stop_order.orderId = parent.orderId + 1
    app.nextorderId += 1
    stop_order.parentId = parent.orderId
    stop_order.transmit = False

# Create stop loss order object
    takeProfit = Order()
    takeProfit.tif = "GTC"
    takeProfit.action = "SELL" if parent.action == "BUY" else "BUY"
    takeProfit.totalQuantity = 5
    takeProfit.orderType = 'LMT'
    takeProfit.lmtPrice = take
    takeProfit.orderId = parent.orderId + 2
    app.nextorderId += 1
    takeProfit.parentId = parent.orderId
    takeProfit.transmit = True



# Place orders
    app.placeOrder(parent.orderId, FX_order(tick), parent)
    app.placeOrder(stop_order.orderId, FX_order(tick), stop_order)
    app.placeOrder(takeProfit.orderId, FX_order(tick), takeProfit)

    time.sleep(8)

    app.disconnect()


#starHere('MOMO', '15.44', '16.00', '14.00')
