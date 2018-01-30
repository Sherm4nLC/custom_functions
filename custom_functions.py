# custom queries

import pandas as pd
import numpy as np
import time
from datetime import datetime as dt
import glob, os
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# json file with google authentication credentials
path_to_key = 'path'

def read_gsheet(gsheet, sheetname, head=1):
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_key, scope)
    client = gspread.authorize(creds)
    
    gsheet = gsheet
    
    sheet = client.open_by_key(gsheet).worksheet(sheetname)
    title = client.open_by_key(gsheet).title
    data = sheet.get_all_records(head=head)
    
    df = pd.DataFrame(data)
    
    return df
    
    

def upload_to_gsheets(df, gsid):

    ### function upload to gsheets
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_key, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(gsid).sheet1
    title = client.open_by_key(gsid).title
    # data = sheet.get_all_records()
    # fx = pd.DataFrame(data)

    for i in range(1,len(df.columns)+1):

        title = df.columns[i-1]

        sheet.update_cell(1,i,title)

    excols = list(string.ascii_uppercase)
    start_range = "2"
    end_range = str(len(df)+2)

    for i, col in enumerate(df.columns):

        range_s = excols[i]+start_range+":"+excols[i]+end_range

        print(range_s)

        cell_list = sheet.range(range_s)
        cell_values = df[col].tolist()

        for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
            cell_list[i].value = val    #use the index on cell_list and the val from cell_values

        sheet.update_cells(cell_list)