# Link to course https://www.youtube.com/watch?v=HXGtLIoiv3Q&list=PLzY2oTkUF1MbgRWZbFlmkTXy8Rb2k-u5r&index=6
# API Ameritrade https://developer.tdameritrade.com/
from keys import ameritrade
import requests, time, re
import os
import pickle as pkl
import pandas as pd

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'company_list.xlsx')

url = 'https://api.tdameritrade.com/v1/instruments'
df = pd.read_excel(my_file)
symbols = df['Symbol'].values.tolist()

#Iterate through the symbol list
start = 0
end = 500
files=[]
while start < len(symbols):
    tickers = symbols[start:end]

    payload = {'apikey': ameritrade,
          'symbol': tickers,
          'projection': 'fundamental'}
    results = requests.get(url, params=payload)
    data = results.json()
    f_name = time.asctime() + '.pkl'   # Automate file creation
    f_name = re.sub('[ :]','_',f_name)
    files.append(f_name)
    with open(f_name, 'wb') as file:
        pkl.dump(data,file)
    start = end
    end += 500
    time.sleep(1)

# Extract and merge information
data=[]
for file in files:
    with open(file,'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    points = ['symbol','netProfitMarginMRQ','peRatio','pegRatio','high52']
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file)  # Delete individual files

points = ['symbol','Margin','PE','PEG','high52']
df_results = pd.DataFrame(data,columns=points)
df_peg = df_results[df_results['PEG']>1]

def view(size):
    start = 0
    stop = size
    while stop  < len(df_peg):
        print(df_peg[start:stop])
        start = stop
        stop += size
    print(df_peg[start:stop])
