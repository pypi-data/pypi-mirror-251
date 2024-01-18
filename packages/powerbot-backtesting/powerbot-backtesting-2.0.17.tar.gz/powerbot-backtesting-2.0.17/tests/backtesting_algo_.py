from datetime import datetime
from pathlib import Path
from powerbot_backtesting import HistoryExporter, BacktestingAlgo
from powerbot_backtesting.utils import generate_input_file

EXCHANGE = "my_exchange"
DELIVERY_AREA = "my_delivery_area"
TIME_FROM = datetime.strptime("2023-06-26 20:00:00", "%Y-%m-%d %H:%M:%S")
TIME_TILL = datetime.strptime("2023-06-26 20:15:00", "%Y-%m-%d %H:%M:%S")
DAY_FROM = datetime.strptime("2023-06-26", "%Y-%m-%d")
DAY_TILL = datetime.strptime("2023-06-26", "%Y-%m-%d")
CONTRACT_TIME = "quarter-hourly"
TIMESTEPS = 15
TIME_UNIT = "minutes"
CACHE_PATH = Path(".")

HIST_API_KEY = "MY_HISTORY_API_KEY"
API_KEY = "MY_API_KEY"
HOST = "MY_API_HOST"


class MyAlgo(BacktestingAlgo):
    def algorithm(self, timestamp, orderbook, key):
        # Buy
        vwap = self.calc_vwap(self.params["trades"], timestamp, "60T-60T-0T")

        if self.params["position"] < 0:
            self.params["position"] = - self.match_orders(
                side="sell",
                orderbook=orderbook,
                timestamp=timestamp,
                price=min(vwap, self.params.get("price", 40)) - 2,
                position=abs(self.params["position"]),
                contract_time=self.params["contract_time"],
                key=key,
                vwap=vwap,
                order_execution="NON")
            return True

        # Sell
        elif self.params["position"] > 0:
            self.params["position"] = self.match_orders(
                side="buy",
                orderbook=orderbook,
                timestamp=timestamp,
                price=max(vwap, self.params.get("price", 40)) + 2,
                position=self.params["position"],
                contract_time=self.params["contract_time"],
                key=key,
                vwap=vwap,
                order_execution="NON")
            return True

        else:
            return False


if __name__ == '__main__':
    # Initialize HistoryExporter
    exporter = HistoryExporter(exchange=EXCHANGE, delivery_area=DELIVERY_AREA, cache_path=CACHE_PATH)

    # Get historic data
    historic_data = exporter.get_historic_data(api_key=HIST_API_KEY,
                                               day_from=DAY_FROM,
                                               day_to=DAY_TILL,
                                               extract_files=True,
                                               process_data=True)

    # Get Contract IDs for specific Timeframe
    contract_ids = exporter.get_contract_ids(
        time_from=TIME_FROM,
        time_till=TIME_TILL,
        contract_time=CONTRACT_TIME
    )

    trade_data = exporter.get_public_trades(contract_ids=contract_ids, contract_time=CONTRACT_TIME, as_csv=True)

    order_data = exporter.get_contract_history(contract_ids=contract_ids, delivery_area=DELIVERY_AREA)

    orderbooks = exporter.get_orderbooks(
        contract_hist_data=order_data,
        timesteps=TIMESTEPS,
        time_unit=TIME_UNIT,
        delivery_area=DELIVERY_AREA,
        use_cached_data=True,
        shortest_interval=True,
        as_json=False)

    ohlc_data = exporter.get_ohlc_data(trade_data, timesteps=15, time_unit="minutes", delivery_area=DELIVERY_AREA, use_cached_data=True)

    if not exporter.cache_path.joinpath("analysis_input", "*.csv").exists():
        # Generate input csv; only need to do once
        generate_input_file(exporter.cache_path.joinpath("analysis_input"))

    else:
        # Instantiate the algo and pass the filled out input file
        algo = MyAlgo(orderbooks=orderbooks,
                      input_file="backtesting_input_1.csv",
                      output_file="backtesting_output_1.csv",
                      trades=trade_data,
                      cache_path=exporter.cache_path)

        # Run the algo
        algo.run()

    exporter.pool.close()
