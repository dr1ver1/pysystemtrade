"""
Purpose: Creates Back-Adjusted Prices from Multiple Prices
Run frequency: Daily schedule
Process dependency: my_multipleprices_from_arcticprices_and_csv_calendars_to_arctic.py has already run
"""

from sysinit.futures.adjustedprices_from_mongo_multiple_to_mongo import process_adjusted_prices_all_instruments


if __name__ == "__main__":
    input("Will overwrite existing prices are you sure?! CTL-C to abort")
    csv_adj_data_path = 'private.data.futures.adjusted_prices_csv'

    # modify flags and datapath as required
    process_adjusted_prices_all_instruments(
        ADD_TO_ARCTIC=True, ADD_TO_CSV=True, csv_adj_data_path=csv_adj_data_path
    )