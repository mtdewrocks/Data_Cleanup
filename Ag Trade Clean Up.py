# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:28:34 2022

@author: shawn
"""

import pandas as pd
import os
import time
##Start timer and change directory

beginningTime = time.time()

os.chdir(r"C:\Users\shawn\Documents\Python Scripts\File Cleanup")

##Establish the Excel file
writer = pd.ExcelWriter(r"Ag Trade Analysis.xlsx", engine='xlsxwriter')

##Read in Files

dfAllAg = pd.read_csv("Ag Products.csv", skiprows=4, skipfooter=2, engine='python')
dfAllAgDollars = pd.read_csv("Ag Products Dollars.csv", skiprows=4, skipfooter=2, engine='python')

##Remove and rename columns, and clean up year column
def quantityCleanUp(df):
    df.drop(columns=['Unnamed: 0', 'Unnamed: 2', 'UOM', 'Reporter Code', 'Partner Code', 'Period/Period %  Change (Qty)', 'Product Code', 'Qty.12'], inplace=True)
    df.rename(columns={'Qty':'January', 'Qty.1':'February', 'Qty.2':'March', 'Qty.3':'April', 'Qty.4':'May', 'Qty.5':'June', 'Qty.6':'July', 'Qty.7':'August', 'Qty.8':'September', 'Qty.9':'October', 'Qty.10':'November', 'Qty.11':'December'}, inplace=True)
    df['Year'] = df['Year'].str[0:4]


def valueCleanUp(df):
    df.drop(columns=['Unnamed: 0', 'Unnamed: 2', 'Reporter Code', 'Partner Code', 'Period/Period %  Change (Value)', 'Product Code', 'Value.12'], inplace=True)
    df.rename(columns={'Value':'January', 'Value.1':'February', 'Value.2':'March', 'Value.3':'April', 'Value.4':'May', 'Value.5':'June', 'Value.6':'July', 'Value.7':'August', 'Value.8':'September', 'Value.9':'October', 'Value.10':'November', 'Value.11':'December'}, inplace=True)
    df['Year'] = df['Year'].astype(str).str[0:4]


quantityCleanUp(dfAllAg)
valueCleanUp(dfAllAgDollars)

##Removes Countries with names ending in '(!)' as they are subsets of a larger country

dfAllAg = dfAllAg[~dfAllAg.Partner.str[-3:].isin(['(!)'])]
dfAllAgDollars = dfAllAgDollars[~dfAllAgDollars.Partner.str[-3:].isin(['(!)'])]

##Remove '(*)' from end of country names as that just signifies that they consist of multiple smaller locations but not critical for charting
removeCharacters = ["(", "*", ")"]
for character in removeCharacters:
    dfAllAg.Partner = dfAllAg.Partner.str.replace(character, "")
    dfAllAgDollars.Partner = dfAllAgDollars.Partner.str.replace(character, "")

##Removes commas and fills in dashes with 0's across each dataframe
def cleanNumbers(frame):
    for col in frame.columns[3:]:
        frame[col] = frame[col].str.replace(",", "")
        frame[col] = frame[col].str.replace("-", "0")
        frame[col] = pd.to_numeric(frame[col])

cleanNumbers(dfAllAg)
cleanNumbers(dfAllAgDollars)

dfAllAg['Product'] = dfAllAg['Product'].str.lstrip()
dfAllAgDollars['Product'] = dfAllAgDollars['Product'].str.lstrip()

 
dfCommodities = pd.concat([dfAllAg])
dfCommodities['Measurement'] = 'Metric Tons'

dfCommodities = pd.melt(dfCommodities, id_vars=['Partner', 'Product', 'Year', 'Measurement'], value_vars=['January', 'February', 'March', 'April',
                                                                                 'May', 'June', 'July', 'August', 'September',
                                                                                 'October', 'November', 'December'], var_name='Month', value_name='Exports')

 
dfCommoditiesDollars = pd.concat([dfAllAgDollars])
dfCommoditiesDollars = pd.melt(dfCommoditiesDollars, id_vars=['Partner', 'Product', 'Year'], value_vars=['January', 'February', 'March', 'April',
                                                                                 'May', 'June', 'July', 'August', 'September',
                                                                                 'October', 'November', 'December'], var_name='Month', value_name='Exports')

 

dfCommodities['Month_Year'] = dfCommodities['Month'] + ' ' + dfCommodities['Year'] 
dfCommoditiesDollars['Month_Year'] = dfCommoditiesDollars['Month'] + ' ' + dfCommoditiesDollars['Year']
dfCommoditiesDollars['Measurement'] = 'Dollars'
dfCombined = dfCommodities.append(dfCommoditiesDollars)
dfCombined['Exports'].fillna(0,inplace=True)
dfCombined['Date'] = pd.to_datetime(dfCombined['Month_Year'])
dfCombined = dfCombined.sort_values(by=['Partner', 'Product', 'Measurement', 'Date'])
dfCombined.reset_index(inplace=True)

grouped = dfCombined.groupby(['Partner', 'Product', 'Measurement'])["Exports"]

dfCombined["Month_Diff"] = grouped.diff()
dfCombined['Year_Diff'] = grouped.diff(periods=12)
dfCombined = dfCombined.drop(columns=['index'])

 
dfAllAg.to_excel(writer, sheet_name='All Ag Commodities - Quantities', index=False)
dfAllAgDollars.to_excel(writer, sheet_name='All Ag Commodities - Dollars', index=False)
dfCombined.to_excel(writer, sheet_name='All Commodity Data', index=False)
writer.save()

endingTime = time.time()
print(endingTime-beginningTime)