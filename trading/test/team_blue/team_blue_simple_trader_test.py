"""
Created on 19.11.2017

Module for testing the SimpleTrader.

@author: rmueller
"""
import unittest
from model.Portfolio import Portfolio
from model.Order import CompanyEnum, OrderList

from utils import read_stock_market_data
from predicting.predictor.reference.perfect_predictor import PerfectPredictor
from definitions import PERIOD_1
from trading.trader.team_blue.team_blue_simple_trader import TeamBlueSimpleTrader


class TeamBlueSimpleTraderTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimpleTrader(self):
        trader = TeamBlueSimpleTrader(PerfectPredictor(CompanyEnum.COMPANY_A), PerfectPredictor(CompanyEnum.COMPANY_B))
        self.assertIsNotNone(trader)
        stock_market_data = read_stock_market_data([CompanyEnum.COMPANY_A], [PERIOD_1])
        self.assertIsNotNone(stock_market_data)
        portfolio = Portfolio(10000, [])
        self.assertIsNotNone(portfolio)

        # Buy stocks based on prediction: With 10000, we can buy 287 stocks A for 34.80 each
        order_list: OrderList = trader.doTrade(portfolio, 0.0, stock_market_data)
        self.assertIsNotNone(order_list)

        self.assertEqual(len(order_list), 0)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TeamBlueSimpleTraderTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
