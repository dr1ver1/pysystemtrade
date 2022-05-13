"""
Purpose: Creates Multiple Prices for each instrument. Loads barchart into arctic. Modifies Roll Calendars
Run frequency: Daily schedule
Process dependency: Load_barchart.py has already run
"""
import sysinit.futures.multipleprices_from_arcticprices_and_csv_calendars_to_arctic as mp
from sysdata.arctic.arctic_futures_per_contract_prices import (
    arcticFuturesContractPriceData,
)
from sysdata.arctic.arctic_spotfx_prices import arcticFxPricesData
from sysobjects.contracts import futuresContract

# Copy callendars!

def arcticInstruments():
    # Prints list of instruments in Arctic
    arctic_prices = arcticFuturesContractPriceData()
    instrument_codes = arctic_prices.get_list_of_instrument_codes_with_price_data()
    print(instrument_codes)
    
    # ['GBPUSD', 'WTI', 'GOLD', 'S&P', 'BUND']
    
    # mydictFuturesContractPrices = arctic_prices.get_all_prices_for_instrument(instrument_code=instrument_code)
    # myContract = futuresContract('WTI', '20220300')
    # myprices = arctic_prices.get_prices_for_contract_object(contract_object=myContract)


def arcticDeleteInstruments():
    # Deletes instruments data from Arctic
    arctic_prices = arcticFuturesContractPriceData()
    instrument_codes = arctic_prices.get_list_of_instrument_codes_with_price_data()
    print(instrument_codes)
    instrument_code = 'GBPUSD'
    arctic_prices.delete_all_prices_for_instrument_code(instrument_code=instrument_code, areyousure=True)
    instrument_code = 'WTI'
    arctic_prices.delete_all_prices_for_instrument_code(instrument_code=instrument_code, areyousure=True)
    instrument_code = 'GOLD'
    arctic_prices.delete_all_prices_for_instrument_code(instrument_code=instrument_code, areyousure=True)
    instrument_code = 'S&P'
    arctic_prices.delete_all_prices_for_instrument_code(instrument_code=instrument_code, areyousure=True)

    instrument_codes = arctic_prices.get_list_of_instrument_codes_with_price_data()
    print(instrument_codes)

def arcticDeleteFXspot():
    # Deletes all FX Spots data from Arctic
    arctic_prices = arcticFxPricesData()
    
    list_of_ccy_codes = arctic_prices.get_list_of_fxcodes()
    arctic_prices.update_fx_prices

    for currency_code in list_of_ccy_codes:
        print('Deleting: ', currency_code)
        arctic_prices.delete_fx_prices(code=currency_code, are_you_sure=True)

def arcticUpdateFXspot():
    # Updates all FX Spots data from Arctic
    arctic_prices = arcticFxPricesData()




if __name__ == "__main__":

    arcticDeleteFXspot()
    exit()
    input("Will overwrite existing prices are you sure?! CTL-C to abort")
    # change: location should be different to my v2 system
    csv_multiple_data_path = "private.data.futures.multiple_prices_csv"

    # change: (initially) should be different to my v2 system
    csv_roll_data_path = "private.data.futures.roll_calendars_csv"

    # mp.process_multiple_prices_all_instruments(
    #     csv_multiple_data_path=csv_multiple_data_path,
    #     csv_roll_data_path=csv_roll_data_path, ADD_TO_ARCTIC=True, ADD_TO_CSV=True
    # )

    instrument_code = 'BUND'
    mp.process_multiple_prices_single_instrument(
        instrument_code,
        csv_multiple_data_path=csv_multiple_data_path,
        csv_roll_data_path=csv_roll_data_path,
        ADD_TO_ARCTIC=True,
        ADD_TO_CSV=True,
    )