#!/usr/bin/env python3

import sys
import os
import yaml
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

def groupbyplot(kind: str, csv_path: str, output_path: str, threshold_others: float, title: str, drop_nan: bool, column_name: str
 ) -> str:
    '''
    Method to group a dataframe by a specific column and count occurences.
    Both a barplot and pie chart can be made by specifying the 'kind'.
    Futhermore a threshold is available to place values below a specific count,
    which will be merged in a group called "Others".
    NaN values can be dropped by setting the corresponding boolean.
    
    '''
    df = pd.read_csv(csv_path, low_memory=False)
    selection = df[column_name].value_counts(dropna=drop_nan)

    # # Fix column names
    columns = {"index":column_name, "size":"Count"}
    selection = selection.to_frame(name="size").reset_index().rename(columns=columns, inplace=False)

    # # Drop low values into "Others" and sum counts
    selection.loc[selection["Count"] < threshold_others, column_name] = "Others"
    selection = selection.groupby(column_name,as_index=False).agg({'Count': 'sum'})
    
    # Create plot
    if kind == "piechart":
        ax = selection.plot(kind="pie", y="Count",\
                                labels=[label for label in selection["Count"].values],\
                                title=title)
        ax.legend(selection[column_name].tolist(), loc="best")
    elif kind == "barplot":
        ax = selection.plot(kind="bar", y="Count", x=column_name,\
                        title=title, rot=0)
    else:
        return "Unknown plot type. Possible values ['piechart', 'barplot']."

    # Save figure
    plt = ax.get_figure()
    plt.savefig(output_path)

    return output_path


if __name__ == "__main__":
    '''
    Script is made specifically for a brane package,
    meaning that input parameters are read from the environment
    variables below. The name of the method has to be specified as
    the command line argument.
    [https://docs.brane-framework.org/]
    '''
    command = sys.argv[1]

    kind = os.environ["INPUT"]
    csv_path = os.environ["CSV_PATH"]
    output_path = os.environ["OUTPUT_PATH"]
    column_name = os.environ["COLUMN_NAME"]
    threshold_others = float(os.environ["THRESHOLD_OTHERS"])
    title = os.environ["PLOT_TITLE"]
    drop_nan = os.environ["DROP_NAN"] in ['true', 'True', True]

    # ##########################################################################################
    # # For testing function (with 'brane --debug test visualization --data data' in CLI)
    # # NOTE: If you want to use the hardcoded values below instead, remove the first '/' in the file paths.
    # kind = "piechart"
    # csv_path = "/data/data/test1000.csv"
    # output_path = "/data/histimg.png"
    # column_name = "Census_PowerPlatformRoleName"
    # threshold_others = float(10)
    # title = "PlatformTypes"
    # drop_nan = True
    # ##########################################################################################

    functions = {
    "groupbyplot": groupbyplot,
    }

    output = functions[command](kind, csv_path, output_path, threshold_others, title, drop_nan, column_name)

    print(yaml.dump({"output": output}))
