#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import yaml

def pie_chart(csv_path: str, output_path: str, column_name: str, threshold_others: float, title: str, drop_nan: bool) -> str:
    df = pd.read_csv(csv_path, low_memory=False)
    platform_types = df[column_name].value_counts(dropna=drop_nan)

    # Fix column names
    columns = {"index":column_name, "size":"Count"}
    platform_types = platform_types.to_frame(name="size").reset_index().rename(columns=columns, inplace=False)

    # Drop low values into "Others" and sum counts
    platform_types.loc[platform_types["Count"] < threshold_others, column_name] = "Others"
    platform_types = platform_types.groupby(column_name,as_index=False).agg({'Count': 'sum'})

    # Create plot
    ax = platform_types.plot(kind="pie", y="Count",\
                            labels=[label for label in platform_types["Count"].values],\
                            title=title)
    ax.legend(platform_types[column_name].tolist(), loc="best")

    # Save figure
    plt = ax.get_figure()
    plt.savefig(output_path)

    return output_path

if __name__ == "__main__":
    command = sys.argv[1]

    input_path = os.environ["INPUT_PATH"]
    output_path = os.environ["FILE"]
    column_name = os.environ["COLUMN_NAME"]
    threshold_others = os.environ["THRESHOLD_OTHERS"]
    title = os.environ["TITLE"]
    drop_nan = os.environ["DROP_NAN"] in ['true', 'True', True]

    # For testing function (with 'brane --debug test visualization --data data' in CLI)
    # input_path = "/data/data/test1000.csv"
    # output_path = "/data/testimg.png"
    # column_name = "Census_PowerPlatformRoleName"
    # threshold_others = 20
    # title = "Platform types"
    # drop_nan = True

    functions = {
    "pie_chart": pie_chart,
    }
    output = functions[command](input_path, output_path, column_name, threshold_others, title, drop_nan)
    print(yaml.dump({"output": output}))
