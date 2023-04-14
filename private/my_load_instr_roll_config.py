# Purpose: Load Instrument Config and Roll Config
# Run Frequency: Ad Hoc. Whenever a new instrument is added; TODO: does it need to be updated whenever there is a roll?
# Process dependency:

# sysinit.instruments_csv_mongo.py has been copy and pasted into this script, in order to modify paths
# sysinit.roll_parameters_csv_mongo.py has been copy and pasted into this script, in order to modify paths

# For instruments_csv_mongo():
# from sysdata.mongodb.mongo_futures_instruments import mongoFuturesInstrumentData
from sysdata.csv.csv_instrument_data import csvFuturesInstrumentData
from sysdata.futures.instruments import futuresInstrumentData

# For roll_parameters_csv_mongo():
from sysdata.mongodb.mongo_roll_data import mongoRollParametersData
from sysdata.csv.csv_roll_parameters import csvRollParametersData

# Load bartchart data into Arctic / Mongo
# 1. Load config for each instrument from instrumentconfig.csv
# 2. Save config data into Mongo
# Any configuration information for these may not be accurate and you use it at your own risk: Review config and update as necessary

# clarify which of these are neeeded:
# GOLD, GOLD_micro, CRUDE_W, CRUDE_W_mini, SP500, SP500_micro

# The first step is to store some instrument configuration information.
# There are two kinds of configuration; instrument configuration and roll configuration.

# Instrument configuration:  static information  to trade an instrument like EDOLLAR: the asset class,
# futures contract point size, and traded currency (it also includes cost levels, that are required in the simulation environment).
# Notice it uses two types of data objects: the object we write to mongoFuturesInstrumentData and the object we read from csvFuturesInstrumentData.
# These objects both inherit from the more generic futuresInstrumentData, and are specialist versions of that.
# You'll see this pattern again and again, and I describe it further in part two of this document.

# Make sure you are running a Mongo Database before running this.
x = futuresInstrumentData()
mdb = mongoFuturesInstrumentData()

# Setting up some instrument configuration
def instruments_csv_mongo():
    INSTRUMENT_CONFIG_PATH = "private.data.futures.csvconfig"
    # Exact copy of code in sysinit.futures.instruments_csv_mongo

    data_out = mongoFuturesInstrumentData()
    data_in = csvFuturesInstrumentData(datapath=INSTRUMENT_CONFIG_PATH)
    print("New data_in: ", data_in)
    instrument_list = data_in.get_list_of_instruments()
    input("Will overwrite existing data are you sure?! CTL-C to abort")
    # modify flags as required
    for instrument_code in instrument_list:
        instrument_object = data_in.get_instrument_data(instrument_code)
        data_out.delete_instrument_data(instrument_code, are_you_sure=True)
        data_out.add_instrument_data(instrument_object)

        # check
        instrument_added = data_out.get_instrument_data(instrument_code)
        print("Added %s to %s" % (instrument_added.instrument_code, data_out))


def roll_parameters_csv_mongo():
    # Roll parameter configuration
    # Populate a mongo DB collection with roll data from a csv

    # The 'priced' contracts are those that we can get prices for, whereas the 'hold' cycle contracts are those we actually hold.
    # 'RollOffsetDays': This indicates how many calendar days before a contract expires that we'd normally like to roll it.
    # These vary from zero (Korean bonds KR3 and KR10 which you can't roll until the expiry date) up to -1100 (Eurodollar where I like to stay several years out on the curve).

    # 'ExpiryOffset': How many days to shift the expiry date in a month, eg (the day of the month that a contract expires)-1.
    # These values are just here so we can build roughly correct roll calendars (of which more later). In live trading you'd get the actual expiry date for each contract.

    # Using these two dates together will indicate when we'd ideally roll an instrument, relative to the first of the month.
    # For example for Bund futures, the ExpiryOffset is 6; the contract notionally expires on day 1+6 = 7th of the month.
    # The RollOffsetDays is -5, so we roll 5 days before this. So we'd normally roll on the 1+6-5 = 2nd day of the month.

    # 'CarryOffset': Whether we take carry from an earlier dated contract (-1, which is preferable) or a later dated contract (+1, which isn't ideal
    # but if we hold the front contract we have no choice). This calculation is done based on the priced roll cycle, so for example
    # for winter crude where the hold roll cycle is just 'Z' (we hold December), and the carry offset is -1 we take the previous month in
    # the priced roll cycle (which is a full year FGHJKMNQUVXZ) i.e. November (whose code is 'X')

    ROLLS_DATAPATH = "private.data.futures.csvconfig"
    input("Will overwrite existing Roll Parameters - are you sure?! CTL-C to abort")
    # modify flags as required

    data_out = mongoRollParametersData()
    data_in = csvRollParametersData(datapath=ROLLS_DATAPATH)

    instrument_list = data_in.get_list_of_instruments()

    for instrument_code in instrument_list:
        instrument_object = data_in.get_roll_parameters(instrument_code)

        data_out.delete_roll_parameters(instrument_code, are_you_sure=True)
        data_out.add_roll_parameters(instrument_code, instrument_object)

        # check
        instrument_added = data_out.get_roll_parameters(instrument_code)
        print("Added %s: %s to %s" % (instrument_code, instrument_added, data_out))


if __name__ == "__main__":
    # instruments_csv_mongo()
    roll_parameters_csv_mongo()
