#!/usr/bin/env python3

# import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import yaml

def pie_chart(csv_path: str, column_name: str, threshold_others: float, title: str, drop_nan: bool) -> str:
    df = pd.read_csv(csv_path, low_memory=False)
    platform_types = df[column_name].value_counts(dropna=drop_nan)

    # Fix column names
    columns = {"index":column_name, "size":"Count"}
    platform_types = platform_types.to_frame(name="size").reset_index().rename(columns=columns, inplace=False)

    # Drop low values into "Others"
    platform_types.loc[platform_types["Count"] < threshold_others, column_name] = "Other platforms"

    # fig = px.pie(platform_types, values="Count", names=column_name, title=title)
    # fig.show()
    fig = plt.figure()

    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    ax.pie(platform_types.index.tolist(), labels = range(len(platform_types.index.tolist())), autopct='%1.2f%%')
    plt.show()

    return "Pie chart created"

if __name__ == "__main__":
    command = sys.argv[1]

    path = os.environ["CSV_PATH"]
    # column_name = os.environ["COLUMN_NAME"]
    # threshold_others = os.environ["THRESHOLD_OTHERS"]
    # title = os.environ["TITLE"]
    # drop_nan = os.environ["PATH"]1

    # path = "/data/test1000.csv"
    column_name = "Census_PowerPlatformRoleName"
    threshold_others = 10
    title = "Platform types"
    drop_nan = True

    functions = {
    "pie_chart": pie_chart,
    }
    output = functions[command](path, column_name, threshold_others, title, drop_nan)
    print(yaml.dump({"output": output}))