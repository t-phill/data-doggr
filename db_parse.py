import pandas as pd 
import numpy as np 
import os
import glob


def parse_excel(files_dir):

    excel_names = glob.glob(f"{files_dir}")

    excels = [pd.ExcelFile(name) for name in excel_names]

    frames = [x.parse(x.sheet_names[0], header=3) for x in excels]

    frames[1:] = [df[1:] for df in frames[1:]]

    combined = pd.concat(frames)

    combined.columns = combined.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    combined.columns = [x.lower() for x in combined.columns]

    combined = combined[pd.notnull(combined['well_type'])]

    combined.to_csv("production.csv", index=False)

    return combined


def sum_parse():

    excel_names = glob.glob("/Users/taylorphillips/galvanize/capstone/sum_file/*.xlsx")

    excels = [pd.ExcelFile(name) for name in excel_names]

    frames = [x.parse(x.sheet_names[0], header=3) for x in excels]

    combined = pd.concat(frames)

    combined.columns = combined.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('#','num')

    combined.columns = [x.lower() for x in combined.columns]

    combined.to_csv("summary.csv", index=False)

    return combined

sum_parse()
parse_excel('/Users/taylorphillips/Downloads/*.xlsx')


