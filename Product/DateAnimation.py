import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
# get latest Vietnam SARS-CoV-2 | COVID-19 data
import io
from io import BytesIO
import datetime

# get data from shared Google Sheet
response = requests.get('https://docs.google.com/spreadsheets/u/1/d/1vkvCEkZ8txrTmEldQGAycVVQbBHV-BwqTaCrxNYTtug/export?format=csv&id=1vkvCEkZ8txrTmEldQGAycVVQbBHV-BwqTaCrxNYTtug&gid=453484829')
assert response.status_code == 200, 'Wrong status code'
data = response.content

# import data to dataframe
df = pd.read_csv(BytesIO(data)) #unprocessed data

# print few rows
df.head()
# print(df)
df['Date'] =pd.to_datetime(df.Date)
dfdata = df['Date'].value_counts().sort_index()
dfDate = pd.DataFrame(dfdata)
# print(dfDate)
nrow,_ = dfDate.shape 
loop = []
a = 0 
for i in range(nrow):
    a += dfDate.iloc[i,0]
    loop.append(a)
dfDate['Cases Over Time'] = loop
dfDate.columns = ['New cases', 'Cases Over Time']
# print(dfDate)

color = ['red', 'green']
fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Cases')
plt.xlabel('Dates')

def buildAnimation(i=int):
    plt.legend(dfDate.columns)
    p = plt.plot(dfDate[:i].index, dfDate[:i].values) #note it only returns the dataset, up to the point i
    for i in range(0,2):
        p[i].set_color(color[i]) #set the colour of each curve
import matplotlib.animation as ani
animator = ani.FuncAnimation(fig, buildAnimation, interval = 100)
plt.show()