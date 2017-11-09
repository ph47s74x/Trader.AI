import copy
import json
import numpy

import Columns
from trading.trader_interface import Portfolio, SharesOfCompany, StockMarketData, TradingAction, TradingActionEnum
from matplotlib import pyplot as plt
import datetime as dt


def read_portfolio(name: str = 'portfolio') -> Portfolio:
    file = open("../json/" + name + ".json")
    json_data = file.read()
    data = json.loads(json_data)
    file.close()

    shares_list = list()
    for share in data['shares']:
        shares_list.append(SharesOfCompany(share['name'], share['amount']))

    # pprint(shares_list[0].companyName)
    # pprint(shares_list[0].amountOfShares)
    # pprint(data['cash'])
    return Portfolio(data['cash'], shares_list)


def read_stock_market_data(name: list, path: str = '../datasets/') -> StockMarketData:
    data = {}
    for symbol in name:
        na_portfolio = numpy.loadtxt(path + symbol + '.csv', dtype='|S15,f8,f8,f8,f8,f8,i8',
                                     delimiter=',', comments="#", skiprows=1)
        dates = list()
        for day in na_portfolio:
            date = dt.datetime.strptime(day[Columns.DATE].decode('UTF-8'), '%Y-%m-%d').date()
            dates.append((date, day[Columns.ADJ_CLOSE]))

        data[symbol] = dates

    return StockMarketData(data)


def update_portfolio(stock_market_data: StockMarketData, portfolio: Portfolio, update: TradingAction):
    updated_portfolio = copy.deepcopy(portfolio)

    print("")

    if update is None:
        print("No action this time")
        return updated_portfolio

    current_date = stock_market_data.get_most_recent_trade_day(update.shares.name)
    current_price = stock_market_data.get_most_recent_price(update.shares.name)

    print(f"Available cash on {current_date}: {updated_portfolio.cash}")
    # for share in update.shares:
    share = updated_portfolio.get_or_insert(update.shares.name)
    # if share.name is update.shares.name:
    amount = update.shares.amount
    trade_volume = amount * current_price

    if update.action is TradingActionEnum.BUY:
        print(f"  Buying {amount} shares of '{share.name}' with an individual value of {current_price}")
        print(f"  Volume of this trade: {trade_volume}")

        if trade_volume <= updated_portfolio.cash:
            share.amount += amount
            updated_portfolio.cash -= trade_volume
        else:
            print(f"  No sufficient cash reserve ({updated_portfolio.cash}) for planned transaction with "
                  f"volume of {trade_volume}")
    elif update.action is TradingActionEnum.SELL:
        print(f"  Selling {amount} shares of {share.name} with individual value of {current_price}")
        print(f"  Volume of this trade: {trade_volume}")

        if share.amount > amount:
            share.amount -= amount
            updated_portfolio.cash += trade_volume
        else:
            print(f"  Not sufficient shares in portfolio ({amount}) for planned sale of {share.amount} shares")

    print(f"Resulting available cash after trade: {updated_portfolio.cash}")

    total_portfolio_value = updated_portfolio.total_value(current_date, stock_market_data.market_data)
    print(f"Total portfolio value after trade: {total_portfolio_value}")
    return updated_portfolio


def draw(portfolio_over_time: dict, prices: StockMarketData):
    plt.figure()

    dates = portfolio_over_time.keys()
    values = [pf.total_value(date, prices.market_data) for date, pf in portfolio_over_time.items()]

    plt.plot(dates, values, color="black")
    plt.show()
