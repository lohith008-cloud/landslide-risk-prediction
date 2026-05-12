import pandas as pd
import yaml

def load_config():

    with open(
        "config/config.yaml",
        "r"
    ) as file:

        return yaml.safe_load(file)

def load_dataset():

    config = load_config()

    df = pd.read_csv(
        config["paths"]["raw_data"]
    )

    return df