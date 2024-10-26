"""
скрипт должен читать data/dataset_.csv,
выбирать оттуда только строки, где есть решение,
писать в новый файл
"""
import pathlib

import pandas


path = str(pathlib.Path(__file__).parent.parent) + "/data/"
fieldnames = ["№", "Topic", "label", "Solution", ""]


def process_xlsx():
    df = pandas.DataFrame()
    file = pandas.read_excel(path + "dataset.xlsx", sheet_name="Sheet1")
    for index, row in file.iterrows():
        if type(row["Solution"]) is not float:
            df = pandas.concat([df, row.to_frame().T], ignore_index=True)

    print(df)
    df.to_csv(path + "out.csv")


if __name__ == "__main__":
    process_xlsx()
