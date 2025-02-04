# Set everything up for Paper Trading

# Set up a new mongodb: do this in a private.yaml file
# Need an exmaple private yaml file, and how to laod and execute it

from time import perf_counter
from typing import Any, Callable


# To do:
# Check file format: My current format. Format from bcutil. Do I need OHL? Check skiprows, skipfooter

BARCHART_DATA_DOWNLOAD_DIRECTORY = "private.data.futures.barchart"


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        func_output = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        print(f"Execution of '{func.__name__}' took: {run_time:.2f}s")
        return func_output

    return wrapper


# Load Barchart Data into MongoDB:
from sysdata.csv.csv_futures_contract_prices import ConfigCsvFuturesPrices
from sysinit.futures.contract_prices_from_csv_to_arctic import (
    init_arctic_with_csv_futures_contract_prices,
    init_arctic_with_csv_futures_contract_prices_for_code,
)

# My format:
# tradeTime,PRICE,Contract,Code,VOLUME,OPEN,HIGH,LOW
# 23/06/2017,0.751,20190600,A6M19,0,0,0,0

# Create a config 'on the fly':
barchart_csv_config = ConfigCsvFuturesPrices(
    input_date_index_name="tradeTime",
    input_skiprows=0,
    input_skipfooter=0,
    input_date_format="%d/%m/%Y",  # Will backslahes work ok?
    input_column_mapping=dict(
        OPEN="OPEN", HIGH="HIGH", LOW="LOW", FINAL="PRICE", VOLUME="VOLUME"
    ),
)


@benchmark
def transfer_barchart_prices_to_arctic(datapath):
    # init_arctic_with_csv_futures_contract_prices(
    #     datapath, csv_config=barchart_csv_config
    # )
    # Just run for a single instrument, for speed
    # TO DO: Check if this end up with duplicate data in monogodb/arctic
    instrument_code = "AUD"
    init_arctic_with_csv_futures_contract_prices_for_code(
        instrument_code, datapath, csv_config=barchart_csv_config
    )


if __name__ == "__main__":
    transfer_barchart_prices_to_arctic(BARCHART_DATA_DOWNLOAD_DIRECTORY)
    pass
