from sysdata.sim.csv_futures_sim_data import csvFuturesSimData

data = csvFuturesSimData()

from systems.provided.rules.ewmac import ewmac_forecast_with_defaults as ewmac

from systems.forecasting import Rules

my_rules = Rules(ewmac)
my_rules.trading_rules()

import pandas as pd
from sysquant.estimators.vol import robust_vol_calc


def calc_ewmac_forecast(price, Lfast, Lslow=None):
    """
    Calculate the ewmac trading rule forecast, given a price and EWMA speeds Lfast, Lslow and vol_lookback

    """
    ## price: This is the stitched price series
    ## We can't use the price of the contract we're trading, or the volatility will be jumpy
    ## And we'll miss out on the rolldown. See https://qoppac.blogspot.com/2015/05/systems-building-futures-rolling.html

    price = price.resample("1B").last()
    if Lslow is None:
        Lslow = 4 * Lfast

    ## We don't need to calculate the decay parameter, just use the span directly

    fast_ewma = price.ewm(span=Lfast).mean()
    slow_ewma = price.ewm(span=Lslow).mean()
    raw_ewmac = fast_ewma - slow_ewma

    vol = robust_vol_calc(price.diff())

    return raw_ewmac / vol


from systems.basesystem import System

my_system = System([my_rules], data)


from systems.trading_rules import TradingRule

ewmac_rule = TradingRule(ewmac)
my_rules = Rules(dict(ewmac=ewmac_rule))


ewmac_8 = TradingRule(
    (ewmac, [], dict(Lfast=8, Lslow=32))
)  ## as a tuple (function, data, other_args) notice the empty element in the middle
ewmac_32 = TradingRule(
    dict(function=ewmac, other_args=dict(Lfast=32, Lslow=128))
)  ## as a dict
my_rules = Rules(dict(ewmac8=ewmac_8, ewmac32=ewmac_32))

my_system = System([my_rules], data)


from sysdata.config.configdata import Config

my_config = Config()
my_config

empty_rules = Rules()
my_config.trading_rules = dict(ewmac8=ewmac_8, ewmac32=ewmac_32)
my_system = System([empty_rules], data, my_config)
print(my_system.rules.get_raw_forecast("EDOLLAR", "ewmac8"))

from systems.forecast_scale_cap import ForecastScaleCap


## By default we pool estimates across instruments. It's worth telling the system what instruments we want to use:
#
my_config.instruments = ["EDOLLAR", "US10", "CORN", "SP500_micro"]

## this parameter ensures we estimate:
my_config.use_forecast_scale_estimates = True

fcs = ForecastScaleCap()
my_system = System([fcs, my_rules], data, my_config)
print(my_system.forecastScaleCap.get_forecast_scalar("EDOLLAR", "ewmac32").tail(5))

my_config.forecast_scalars = dict(ewmac8=5.3, ewmac32=2.65)

## this parameter ensures we don't estimate:
my_config.use_forecast_scale_estimates = False

my_system = System([fcs, empty_rules], data, my_config)

print(my_system.forecastScaleCap.get_forecast_scalar("EDOLLAR", "ewmac32"))


my_system.forecastScaleCap.get_capped_forecast("EDOLLAR", "ewmac32")

from systems.forecast_combine import ForecastCombine

combiner = ForecastCombine()
my_system = System([fcs, empty_rules, combiner], data, my_config)
my_system.combForecast.get_forecast_weights("EDOLLAR").tail(5)
my_system.combForecast.get_forecast_diversification_multiplier("EDOLLAR").tail(5)

from systems.rawdata import RawData
from systems.positionsizing import PositionSizing
from systems.accounts.accounts_stage import Account

combiner = ForecastCombine()
raw_data = RawData()
position_size = PositionSizing()
my_account = Account()

## let's use naive markowitz to get more interesting results...
my_config.forecast_weight_estimate = dict(method="one_period")
my_config.use_forecast_weight_estimates = True
my_config.use_forecast_div_mult_estimates = True

combiner = ForecastCombine()
my_system = System(
    [my_account, fcs, my_rules, combiner, position_size, raw_data], data, my_config
)

## this is a bit slow, better to know what's going on
my_system.set_logging_level("on")

cbf = my_system.combForecast
fw = cbf.get_forecast_weights("US10")
print(fw.tail(5))
print(my_system.combForecast.get_forecast_weights("US10").tail(5))


print(my_system.combForecast.get_forecast_diversification_multiplier("US10").tail(5))
