import pandas as pd 
import numpy as np 
import os
import glob


def parse_excel(files_dir):
    '''
    input : directory to scraped excel files utilizing 'glob' search of all .xlsx files
            e.g. ('/Users/username/Downloads/*.xlsx')

    return: pandas dataframe

    export: csv file 'production.csv'
    '''
    #list of file names
    excel_names = glob.glob(f"{files_dir}")

    #creating excelfile object for each .xlsx file
    excels = [pd.ExcelFile(name) for name in excel_names]

    #list of dataframes for each excelfile object
    frames = [x.parse(x.sheet_names[0], header=3) for x in excels]

    #remove header from each file except for the first
    frames[1:] = [df[1:] for df in frames[1:]]

    combined = pd.concat(frames)

    #manipulate headers for easier input into postgres tables
    combined.columns = combined.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    combined.columns = [x.lower() for x in combined.columns]

    #There is a yearly total row for each year in the well histories..
    #Removing these rows by using condition in well_type column
    combined = combined[pd.notnull(combined['well_type'])]

    #exporting dataframe to csv file
    combined.to_csv("production.csv", index=False)

    return combined


def sum_parse():

    '''
    input : directory to summary excel file using 'glob'

    return: pandas dataframe

    export: csv file 'summary.csv'
    '''

    excel_names = glob.glob("/Users/taylorphillips/galvanize/capstone/data/*.xlsx")

    excels = [pd.ExcelFile(name) for name in excel_names]

    frames = [x.parse(x.sheet_names[0], header=3) for x in excels]

    combined = pd.concat(frames)

    combined.columns = combined.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('#','num')

    combined.columns = [x.lower() for x in combined.columns]

    combined.to_csv("summary.csv", index=False)

    return combined



