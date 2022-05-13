# Purpose: Load barchart csv files, but using my format and path
# Run Frequency: Daily schedule
# Process dependency: Latest Barchart data already saved into csv files, with column and filename requiremets as per code below

import sysinit.futures.barchart_futures_contract_prices as bc


# XXMYY_Barchart_Interactive_Chart*.csv Where XX is the two character barchart instrument identifier, 
# eg ZW is Wheat, M is the future contract month (F=January, G=February... Z =December), YY is the two digit year code, and the rest is fluff. 
# The little function strip_file_names renames them so they have the expected format: NNNN_YYYYMMDD.csv, 
# where NNNN is my instrument code (at least four letters and usually way more), and YYYYMM00 is a numeric date format eg 20201200 
# Options:
# 1. rename existing files to expected input name format: XXMYY_blah.csv, call transfer_barchart_prices_to_arctic
#** -> 2. rename existing files to expected output name format: NNNN_YYYYMMDD.csv, init_arctic_with_csv_futures_contract_prices



# Override and modify barchart_csv_config:
barchart_csv_config = bc.ConfigCsvFuturesPrices(
    input_date_index_name="tradeTime",
    input_skiprows=0,
    input_skipfooter=0,
    input_date_format="%d/%m/%Y",
    input_column_mapping=dict(
        FINAL="PRICE", VOLUME="VOLUME", OPEN="OPEN", HIGH="HIGH", LOW="LOW"
    ),
)


if __name__ == "__main__":
    # input("Will overwrite existing prices are you sure?! CTL-C to abort")
    # modify flags as required
    datapath = "private.data.futures.barchart"
    # bc.transfer_barchart_prices_to_arctic(datapath)
    bc.init_arctic_with_csv_futures_contract_prices(datapath=datapath, csv_config=barchart_csv_config)