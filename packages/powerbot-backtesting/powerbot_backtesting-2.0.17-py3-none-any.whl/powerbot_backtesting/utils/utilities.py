import certifi
import pandas as pd
from powerbot_client import ApiClient, Configuration
from pathlib import Path


def init_client(api_key: str, host: str) -> ApiClient:
    """
    Initializes PowerBot Client to enable data requests by the API.

    Args:
        api_key (str): API Key for PowerBot
        host (str): Host URL for PowerBot

    Returns:
        PowerBot ApiClient Object
    """
    config = Configuration(api_key={'api_key_security': api_key}, host=host, ssl_ca_cert=certifi.where())
    return ApiClient(config)


def generate_input_file(cache_path: Path):
    """
    Generates a csv file to put positions and signals into to use with the BacktestingAlgo

    Args:
        cache_path (Path): The cache_path

    Returns:
        csv file
    """
    # File creation
    input_file = pd.DataFrame([{"delivery_start": "%Y-%m-%dT%H-%M%z",
                                "delivery_end": "%Y-%m-%dT%H-%M%z",
                                "position": 10,
                                "price": 100}])

    # Caching
    cache_path.mkdir(parents=True, exist_ok=True)

    # File name
    f_count = 1
    while cache_path.joinpath(f"backtesting_input_{f_count}.csv").exists():
        f_count += 1
    input_file.to_csv(cache_path.joinpath(f"backtesting_input_{f_count}.csv"), sep=";", index=False)
