#!/usr/bin/env python3
# _coding_: utf8

import json
import sys
import time
import traceback
import random as rd
import pandas as pd
from threading import Thread
from broker.client import BrokerClient


class icoMarketMaking(object):

    def __init__(self, symbol, pm):
        self.symbol = symbol
        self.pm = pm

        self.api = BrokerClient(entry_point=self.pm.get('entry_point', 'https://api.bhex.com/openapi/'), api_key=self.pm['api_key'], secret=self.pm['secret'])

        # self.api = BhexClient(api_key=self.pm['api_key'], secret=self.pm['secret'], entry_point=self.pm.get('entry_point', 'https://api.bhex.com/openapi/'))
        self.imitate_symbol = self.pm.get('imitate_symbol', '')

        # load order config file
        self.tgtStructBid = pd.DataFrame.from_dict(self.pm['tgtStructBid'])
        self.tgtStructAsk = pd.DataFrame.from_dict(self.pm['tgtStructAsk'])
        # print(self.tgtStructBid.loc[str(1), 'fromBestBid'], self.tgtStructAsk)

        self.orderThread = None
        self.klineThread = None

    def start(self):
        orders = self.api.open_orders(symbol=self.symbol, limit=1000)
        self.tgtStructBid['cid'] = [''] * len(self.tgtStructBid)
        self.tgtStructAsk['cid'] = [''] * len(self.tgtStructAsk)

        orders = sorted(orders, key=lambda x: float(x['price']), reverse=True)
        i = 0
        for o in orders:
            if o['side'] == 'BUY' and o['clientOrderId'][:len(self.pm['orderPrefix'])] == self.pm['orderPrefix']:
                if i < self.pm['orderNum']:
                    self.tgtStructBid.loc[str(i), 'cid'] = o['clientOrderId']
                    i += 1
                else:
                    self.api.order_cancel(client_order_id=o['clientOrderId'])

        i = 0
        for o in reversed(orders):
            if o['side'] == 'SELL' and o['clientOrderId'][:len(self.pm['orderPrefix'])] == self.pm['orderPrefix']:
                if i < self.pm['orderNum']:
                    self.tgtStructAsk.loc[str(i), 'cid'] = o['clientOrderId']
                    i += 1
                else:
                    self.api.order_cancel(client_order_id=o['clientOrderId'])

        self.orderThread = Thread(target=self.orderWorker)
        self.orderThread.start()

        self.klineThread = Thread(target=self.drawKline)
        self.klineThread.start()

    # to calculate the fair bid/ask price
    def getFairPrice(self):
        try:
            depth = self.api.depth(symbol=self.symbol, limit=100)
            print(str(depth['bids']))
            bids = depth['bids']
            pqsum = qsum = 0
            for b in bids:
                qsum += float(b[1])
                pqsum += float(b[0]) * float(b[1])
                if qsum >= self.pm['fairBidPriceQty']:
                    break
            fair_bid_price = pqsum / qsum

            asks = depth['asks']
            pqsum = qsum = 0
            for a in asks:
                qsum += float(a[1])
                pqsum += float(a[0]) * float(a[1])
                if qsum >= self.pm['fairAskPriceQty']:
                    break
            fair_ask_price = pqsum / qsum

            if self.imitate_symbol:
                tgt = self.api.klines(symbol=self.imitate_symbol, limit=1)[0]
                chg = float(tgt[4]) / float(tgt[1])
                fair_bid_price *= chg
                fair_ask_price *= chg

            return fair_bid_price, fair_ask_price
        except:
            traceback.print_exc()

    # order placing fn, will check one pair of bid and ask at one time
    def orderWorker(self):
        while True:
            for i in reversed(range(self.pm['orderNum'])):
                print(i)
                try:
                    fair_bid_price, fair_ask_price = self.getFairPrice()
                    # print(fair_bid_price, fair_ask_price)
                    fair_mid_price = 0.5 * (fair_bid_price + fair_ask_price)
                    best_bid = fair_mid_price * (1 - self.pm['bid_spread'])
                    best_ask = fair_mid_price * (1 + self.pm['ask_spread'])

                    send_flag = True
                    price = best_bid * (1 - self.tgtStructBid.loc[str(i), 'fromBestBid'])
                    order = self.api.order_get(orig_client_order_id=self.tgtStructBid.loc[str(i), 'cid'])
                    print(str(order))
                    try:
                        if order['status'] == 'FILLED':
                            None
                        elif abs(float(order['price']) - price) > 0.0005 * price:
                            self.api.order_cancel(client_order_id=self.tgtStructBid.loc[str(i), 'cid'])
                        else:
                            send_flag = False
                    except:
                        traceback.print_exc()
                        print(order)

                    if send_flag:
                        params = {'symbol': self.symbol, 'side': 'BUY', 'type': 'LIMIT_MAKER',
                                  'quantity': self.pm['orderQty'] * self.tgtStructBid.loc[str(i), 'qtyMultiplier'] * (
                                          1 + 0.6 * (rd.random() - 0.5)),
                                  'price': price * (1 + 0.0005 * (rd.random() - 0.5)),
                                  'newClientOrderId': self.pm['orderPrefix'] + str(int(time.time() * 1000)) + 'b' + str(i)}
                        self.prepareOrder(params)
                        self.tgtStructBid.loc[str(i), 'cid'] = params['newClientOrderId']

                    send_flag = True
                    price = best_ask * (1 + self.tgtStructAsk.loc[str(i), 'fromBestAsk'])
                    order = self.api.order_get(orig_client_order_id=self.tgtStructAsk.loc[str(i), 'cid'])
                    try:
                        if order['status'] == 'FILLED':
                            None
                        elif abs(float(order['price']) - price) > 0.0005 * price:
                            self.api.order_cancel(client_order_id=self.tgtStructAsk.loc[str(i), 'cid'])
                        else:
                            send_flag = False
                    except:
                        traceback.print_exc()
                        print(order)

                    if send_flag:
                        params = {'symbol': self.symbol, 'side': 'SELL', 'type': 'LIMIT_MAKER',
                                  'quantity': self.pm['orderQty'] * self.tgtStructAsk.loc[str(i), 'qtyMultiplier'] * (
                                          1 + 0.6 * (rd.random() - 0.5)),
                                  'price': price * (1 + 0.0005 * (rd.random() - 0.5)),
                                  'newClientOrderId': self.pm['orderPrefix'] + str(int(time.time() * 1000)) + 'a' + str(i)}
                        self.prepareOrder(params)
                        self.tgtStructAsk.loc[str(i), 'cid'] = params['newClientOrderId']

                except:
                    traceback.print_exc()

                time.sleep(self.pm.get('orderRefreshInterval', 5))

    # draw k line fn
    def drawKline(self):
        while True:
            try:
                res = self.api.ticker_24hr(symbol=self.symbol)
                # print(res)
                best_bid = float(res['bestBidPrice'])
                best_ask = float(res['bestAskPrice'])

                cid = str(int(time.time()))

                order = {'symbol': self.symbol,
                         'quantity': self.pm['orderQty'] * (0.2 + 1.6 * rd.random()),
                         'price': round(best_bid + (best_ask - best_bid) * rd.random(), self.pm['priceDecimalLength']),
                         'newClientOrderId': cid}

                qty = order['quantity']

                if best_bid + 0.5 * (best_ask - best_bid) < order['price'] < best_ask or order['price'] == best_ask:
                    order['side'] = 'SELL'
                    order['type'] = 'LIMIT_MAKER'
                    self.prepareOrder(order)
                    # time.sleep(3 + 7 * rd.random())
                    order.pop('newClientOrderId')
                    order['side'] = 'BUY'
                    order['type'] = 'LIMIT'
                    order['timeInForce'] = 'IOC'
                    order['quantity'] = qty * (0.1 + 0.8 * rd.random())
                    self.prepareOrder(order)
                    # time.sleep(2 + 5 * rd.random())
                    if rd.random() < 0.2:
                        order['quantity'] = qty - order['quantity']
                        self.prepareOrder(order)
                    self.api.order_cancel(client_order_id=cid)

                elif best_bid < order['price'] < best_bid + 0.5 * (best_ask - best_bid) or order['price'] == best_bid:
                    order['side'] = 'BUY'
                    order['type'] = 'LIMIT_MAKER'
                    self.prepareOrder(order)
                    # time.sleep(3 + 7 * rd.random())
                    order.pop('newClientOrderId')
                    order['side'] = 'SELL'
                    order['type'] = 'LIMIT'
                    order['timeInForce'] = 'IOC'
                    order['quantity'] = qty * (0.1 + 0.8 * rd.random())
                    self.prepareOrder(order)
                    # time.sleep(2 + 5 * rd.random())
                    if rd.random() < 0.2:
                        order['quantity'] = qty - order['quantity']
                        self.prepareOrder(order)
                    self.api.order_cancel(client_order_id=cid)

            except:
                traceback.print_exc()
                print(res)

            time.sleep(10 + 30 * rd.random())

    # random cancel order fn
    def randomCancel(self):
        try:
            orders = self.api.open_orders(symbol=self.symbol, limit=1000)
            i = int(rd.random() * len(orders))
            self.api.order_cancel(client_order_id=orders[i]['clientOrderId'])
            print('randomCancel', orders[i])
        except:
            traceback.print_exc()

    # send order fn
    def prepareOrder(self, params):
        params['price'] = round(params['price'], self.pm['priceDecimalLength'])
        params['quantity'] = round(params['quantity'], self.pm['qtyDecimalLength'])
        res = self.api.order_new(**params)
        if res.get('msg', '') == 'Balance insufficient ':
            print(res, params)
            self.randomCancel()
            print(self.api.account())
        elif 'msg' in res:
            print(res, params)
        # else:
        #     print(res, params)


if __name__ == '__main__':

    # try:
    #     symbol = str.upper(sys.argv[1])
    # except:
    #     symbol = ''
    #     print("NEED SYMBOL")
    #     exit(0)

    symbol = 'EEGUSDT'

    with open("parameter.json") as f:
        json_file = json.load(f)

    a = icoMarketMaking(symbol=symbol,
                        pm=json_file[symbol])

    a.start()
