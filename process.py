import pandas as pd
from ETF import get_ETF_performance, get_ETF_asx_list
import numpy as np

# Write HTML table for ETF data

alldata, lst_upd =get_ETF_performance()

dfp = pd.DataFrame(alldata[1:], columns=[x.strip() for x in alldata[0]])
dfp.drop(['Add toPortfolio','Name', '6 moReturn%'],axis=1, inplace=True)
dfp.rename(columns = {'1 yrReturn%': '1 Yr', '3 yrReturn%': '3 Yr', 'YTDReturn%':'YTD'}, inplace=True)
alldata, headers, links = get_ETF_asx_list()


df = pd.DataFrame(alldata, columns=headers)
df['iNAV'] = df['iNAV'].str.replace('\n',', ')
df['Admission Date'] = pd.to_datetime(df['Admission Date'])
df['Exposure']  = links
df = df.merge(dfp, left_on='ASX Code', right_on='ASX code', how='left')
df.drop('ASX code',axis=1, inplace=True)

df['1 Yr'] = df['1 Yr'].str.replace('-- ','0') 
df['3 Yr'] = df['3 Yr'].str.replace('-- ','0') 
df['YTD'] = df['YTD'].str.replace('-- ','0') 

df['1 Yr'] = df['1 Yr'].astype('float') 
df['3 Yr'] = df['3 Yr'].astype('float')
df['YTD'] = df['YTD'].astype('float')
df['Management Cost %'] = df['Management Cost %'].astype('float')

html = df.to_html(table_id='sampleTable', render_links=True, escape=False)
fid = open("df.html","w")
fid.write(html)
fid.close()

fid = open("upd.txt","w")
fid.write(lst_upd)
fid.close()





