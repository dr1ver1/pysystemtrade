## run_daily_price_updates()

### Check for defaults.yaml or overriden in private_config
### 
### Questions:
- what is dataControlProcess vs diagControlProcess?
- run_daily_prices_updates

### Functions
fn: run_daily_price_updates():
    obj: data = dataBlob
    fn: get_list_of_timer_functions_for_price_update()
    obj: price_process = processToRun(process_name, data, list_of_timer_names_and_functions)
    meth: price_process.run_process()

fn: get_list_of_timer_functions_for_price_update()
    obj: data_historical = dataBlob
    obj: historical_update_object = updateHistoricalPrices()
    return list_of_timer_names_and_functions = [
        ("update_historical_prices", historical_update_object),
    ] # This is a list of tuples: (name and object to be called)
    # The object is called by a timer

price_process = processToRun(process_name, data, list_of_timer_names_and_functions)
    
class processToRun
meth: processToRun::self.__init__()
    copy passed variables to self variables
    self._setup()

meth: processToRun::self._setup()
    self.data.log.setup(type=self.process_name) # Creates a copy of the log (which log?) but with type=self.process_name
    self._log = self.data.log

    data_control = dataControlProcess(self.data)
    self._data_control = data_control
    diag_process = diagControlProcess(self.data)
    self._diag_process = diag_process

    wait_reporter = reportProcessStatus(self.log)
    self._wait_reporter = wait_reporter

what is dataControlProcess vs diagControlProcess?
dataControlProcess methods:
check_if_okay_to_start_process, start_process, check_if_should_pause_process, finish_process
finish_all_processes, check_if_pid_running_and_if_not_finish_all_processes, 
check_if_process_status_stopped, change_status_to_stop, change_status_to_go, 
change_status_to_no_run, change_status_to_pause, has_process_finished_in_last_day, 
log_start_run_for_method, log_end_run_for_method

diagControlProcess methods:
get_config_dict, get_process_status_dict, has_previous_process_finished_in_last_day, 
is_it_time_to_run, is_it_time_to_stop, get_method_timer_parameters, 
does_method_run_on_completion_only, frequency_for_process_and_method, 
max_executions_for_process_and_method, get_method_configuration_for_process_name, 
get_list_of_methods_for_process_name, get_all_method_dict_for_process_name, 
previous_process_name, get_start_time, 
how_long_in_hours_before_trading_process_finishes, get_stop_time_of_trading_process, 
get_stop_time, _get_configuration_item_for_process_name, 
get_process_configuration_for_item_name, when_method_last_started, 
when_method_last_ended, method_currently_running, get_control_for_process_name, 
get_list_of_process_names, get_configured_kwargs_for_process_name_and_methods_that_run_on_completion, 



meth: price_process.run_process()


updateHistoricalPrices(data_historical)
Context: run_daily_price_updates.py::get_list_of_timer_functions_for_price_update()
meth: update_historical_prices(self, download_by_zone: dict = arg_not_supplied)
def update_historical_prices_with_data
    if download_by_zone is arg_not_supplied:
        download_all_instrument_prices_now(data)

fn: download_all_instrument_prices_now(data: dataBlob):
    price_data = diagPrices(data)

    list_of_instrument_codes = price_data.get_list_of_instruments_in_multiple_prices()
    update_historical_prices_for_list_of_instrument_codes(
        data=data,
        list_of_instrument_codes=list_of_instrument_codes,
    )

Context: 
diagPrices: 
meth: get_list_of_instruments_in_multiple_prices
    list_of_instruments = (
        self.db_futures_multiple_prices_data.get_list_of_instruments()
    )
    if ignore_stale:
        list_of_instruments = self.remove_stale_instruments(list_of_instruments)

    return list_of_instruments

meth: def db_futures_multiple_prices_data(self) -> futuresMultiplePricesData:
        return self.data.db_futures_multiple_prices

data.db_futures_multiple_prices comes from the datablob


```mermaid
flowchartrun_daily_price_updates()
participant Client
```