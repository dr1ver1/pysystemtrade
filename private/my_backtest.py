from datetime import datetime
from tracemalloc import stop
from sysdata.config.configdata import Config    # imports the Config class
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import pandas as pd
import os
from systems.trading_rules import TradingRule


from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
# from sysdata.csv.csv_roll_calendars import csvRollCalendarData


def createCSVs(instr):

    startDate = '2016-01-01'
    
    # Main: 
    results = system.positionSize.get_underlying_price(instr).loc[startDate:].to_frame()

    i=1
    
    results = pd.merge(results, system.positionSize.get_instrument_currency_vol(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='currencyVol'

    i+=1
    results = pd.merge(results, system.positionSize.get_instrument_value_vol(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='instrVol'

    i+=1
    results = pd.merge(results, system.positionSize.get_volatility_scalar(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='volScalar'

    i+=1
    results = pd.merge(results, system.positionSize.get_subsystem_position(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='subsysPos'

    i+=1
    results = pd.merge(results, system.accounts.get_notional_position(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='notionalPos'

    i+=1
    results = pd.merge(results, system.accounts.get_actual_position(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='actualPos'

    i+=1
    results = pd.merge(results, system.rawdata.daily_annualised_roll(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='dlyAnnRoll'

    i+=1
    results = pd.merge(results, system.positionSize.get_block_value(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='block'
    
    i+=1
    results = pd.merge(results, system.rawdata.raw_carry(instr).loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='rawCarry'

    i+=1
    results = pd.merge(results, system.positionSize.get_fx_rate(instr).loc[startDate:].resample('1B').last().to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='FXrate'
    
    i+=1
    results = pd.merge(results, system.rawdata.raw_futures_roll(instr).loc[startDate:].resample('1B').mean().to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='rawFuturesRoll'

    i+=1
    results = pd.merge(results, system.rawdata.annualised_roll(instr).loc[startDate:].resample('1B').last().to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='annRoll'
   
    # Carry
    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_raw_forecast(instr, "carry").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_RawFC'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_forecast_scalar(instr, "carry").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_FCScalar'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_scaled_forecast(instr, "carry").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_scaledFC'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_capped_forecast(instr, "carry").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_cappedFC'
    
    i+=1
    results = pd.merge(results, system.accounts.pandl_for_instrument_forecast(instr,"carry").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_PLinstrFC'

    i+=1
    results = pd.merge(results, system.accounts.pandl_for_instrument_forecast(instr,"carry").percent.loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_PLinstrFCpct'

    i+=1
    results = pd.merge(results, 
        system.accounts.pandl_for_instrument_forecast(instr,"carry").percent.curve().loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_Curve_pct'

    # CarryOLD
    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_raw_forecast(instr, "carryOLD").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_RawFC'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_forecast_scalar(instr, "carryOLD").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_FCScalar'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_scaled_forecast(instr, "carryOLD").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_scaledFC'

    i+=1
    results = pd.merge(results, system.forecastScaleCap.get_capped_forecast(instr, "carryOLD").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_cappedFC'
    
    i+=1
    results = pd.merge(results, system.accounts.pandl_for_instrument_forecast(instr,"carryOLD").loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_PLinstrFC'

    i+=1
    results = pd.merge(results, system.accounts.pandl_for_instrument_forecast(instr,"carryOLD").percent.loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_PLinstrFCpct'

    i+=1
    results = pd.merge(results, 
        system.accounts.pandl_for_instrument_forecast(instr,"carryOLD").percent.curve().loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_Curve_pct'
    

    i+=1
    results = pd.merge(results, 
        system.accounts.pandl_for_instrument_forecast(instr,"carryOLD").curve().loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='CarryOLD_Curve'
    
    i+=1
    results = pd.merge(results, 
        system.accounts.pandl_for_instrument_forecast(instr,"carry").curve().loc[startDate:].to_frame(), 
        left_index=True, right_index=True, how="left")
    results.columns.values[i]='Carry_Curve'


    results = pd.merge(results, system.rawdata.get_instrument_raw_carry_data(instr).loc[startDate:].resample('1B').last(), 
        left_index=True, right_index=True, how="left")    # 4 cols (+ index)

    results.columns.values[0]='price1'


    resultsFile = instr + '_results.csv'
    resultsPath = '/mnt/leopard/samba/trading/Working/'
    fullPath = os.path.join(resultsPath, resultsFile)

    # results.to_csv('/mnt/leopard/samba/trading/Working/results.csv', date_format='%d/%m/%Y')
    results.to_csv(fullPath, date_format='%d/%m/%Y')

    
    print()

    # Single value
    # system.accounts.subsystem_turnover(instr) 
    # system.accounts.instrument_turnover(instr)
    # system.accounts.forecast_turnover(instr, "carry")
    # system.accounts.get_SR_cost_for_instrument_forecast(instr, "carry")
    # system.rawdata.roll_differentials(instr).loc['2021-01-01':]
    # system.positionSize.get_daily_cash_vol_target()

def carryOLD(raw_carry):
    return raw_carry
    
    

if __name__ == '__main__':
    loadPickle = True
    myData = False

    # csvFuturesInstrumentData  - config and costs: Leave as default

    # csvFuturesMultiplePricesData - prices for current, next and carry contracts
    # csvFuturesAdjustedPricesData - stitched back-adjusted prices
    # csvFxPricesData - FX prices
    if myData:
        data=csvFuturesSimData(csv_data_paths = dict(csvFuturesMultiplePricesData="private.data.futures.multiple_prices_csv", 
            csvFuturesAdjustedPricesData="private.data.futures.adjusted_prices_csv",
            csvFxPricesData="private.data.spot.barchart"))
    else:
        data=csvFuturesSimData() # default data sources

    # data.db_futures_adjusted_prices_data
    # data.db_futures_instrument_data
    # data.db_futures_multiple_prices_data
    # data.db_fx_prices_data

    print()
    instr = 'SP500_micro'
    # CRUDE_W_mini: 0.20
    # GOLD_micro: 0.20
    # GBP: 0.20
    # BUND: 0.20
    # SP500_micro: 0.20

    # import pandas as pd
    # what are we getting from this 2nd import? A: Structure of a system, not specifics:
    # System with stages: accounts, portfolio, positionSize, rawdata, combForecast, forecastScaleCap, rules
    # Specifics are in config.yaml



    my_config=Config("private.test_system1.config2.yaml")   # How does pickling impact this?
    system=futures_system(data=data, config=my_config, log_level='on')

    if loadPickle:
        system.cache.unpickle("private.test_system1.system2.pck")

    # what to change in config.yaml?
    # Instruments and weights
    # Q: Where is the data coming from?
    # Start with fixed params, then change to estimated params

    # Intermediate results:
    print(system.rules.get_raw_forecast(instr, "ewmac64_256"))
    print(system)
    # stage_name.methods()



    print((system.get_instrument_list()))
    print(system.accounts.portfolio().stats()) ## see some statistics

    # If the pickle wasn't loaded, then save it. It it was loaded, then no need to save it:
    if not loadPickle:
        system.cache.pickle("private.test_system1.system2.pck")

    fig, axes = plt.subplots(nrows=4, ncols=1)

    # system.accounts.portfolio().curve().plot(ax=axes[0])
    i=0
    system.accounts.pandl_for_instrument(instr).curve().plot(ax=axes[i])
    
    i=i+1
    system.data.get_raw_price(instr).plot(ax=axes[i])
    
    i=i+1
    system.forecastScaleCap.get_capped_forecast(instr,"carry").plot(ax=axes[i])

    i=i+1
    system.forecastScaleCap.get_capped_forecast(instr,"carryOLD").plot(ax=axes[i])

    # fig = plt.gcf()
    createCSVs(instr)
    fig.show()

    print(system.accounts.pandl_for_instrument(instr).percent.stats()) ## produce % statistics 
    print(system.accounts.pandl_for_instrument_forecast(instr, "carry").sharpe()) ## Sharpe for a specific trading rule variation
    pass

    exit()

