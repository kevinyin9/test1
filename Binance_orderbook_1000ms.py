#!/usr/bin/env python
# coding: utf-8

# In[19]:


import websocket
import _thread
import time
from websocket import WebSocketApp
import requests
import json
import pandas as pd
import csv


# In[20]:


socket='wss://stream.binance.com:9443/ws/btcusdt@depth@1000ms'


# In[25]:


data = {'Timestamp':[],'data':[]}
res = pd.DataFrame(data)
res.to_csv("Binance_orderbook_10s.csv", header=True, index=False, mode="a")
    


# In[26]:


res = requests.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=100')
temp = res.json()
orderbook = {'bids':{},
            'asks':{}}
temp_bids, temp_asks= {}, {}
for i in temp['bids']:
    temp_bids.update({i[0]:i[1]})
for i in temp['asks']:
    temp_asks.update({i[0]:i[1]})
#orderbook['lastUpdateId'] = temp['lastUpdateId']
orderbook['bids'].update(temp_bids)
orderbook['asks'].update(temp_asks)
#for key in orderbook:
    #print(key)
    #print(orderbook[key])
print(orderbook)


# In[54]:


rep=0
def on_message(ws,message):
    global orderbook
    global rep
    msg=json.loads(message)
    print(rep)
    if (rep == 10): 
        print(10)
        bid_dict={}
        ask_dict={}
        for i in msg['b']:
            bid_dict.update({i[0]:i[1]})
        for i in msg['a']:
            ask_dict.update({i[0]:i[1]})
        #orderbook['lastUpdateId']=msg['u']
        orderbook['bids'].update(bid_dict)
        orderbook['asks'].update(ask_dict)
        orderbook['bids']={key:val for key, val in orderbook['bids'].items() if val !='0.00000000'}
        orderbook['asks']={key:val for key, val in orderbook['asks'].items() if val !='0.00000000'}
        print(orderbook)
        time=msg['E']
        with open('Binance_orderbook_10s.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([time, orderbook])
            print('Write into csv file...')
            rep=0
        
    rep+=1

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(socket,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
ws.run_forever()


# In[49]:





# In[25]:





# In[ ]:




