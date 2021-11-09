# -*- coding: utf-8 -*-
import pandas as pd
import threading
import time
import json
from pandas import json_normalize
def get_lists(datas, times, title):
    p = []
    s = []
    t = []
    for idx, data in enumerate(datas):
        for  (price, size) in data:
            t.append(times[idx])
            p.append(price)
            if size < 1e-4:
                size = format(size, '.8f')
            s.append(size)
    df = pd.DataFrame({title+"_price":p,
                    title+"_size":s,
                    title+"_time":t})
    return df

def to_csv(asks, bids, times):
    ask_df = get_lists(asks, times, "asks")
    bids_df = get_lists(bids, times, "bids")
    res = pd.concat([ask_df, bids_df], axis=1)
    
    print("... Write into csv file ...")
    print("  Asks size: " + str(len(ask_df)))
    print("  Bids size: " + str(len(bids_df)))
    #res.to_csv("BTCUSDT_SPOT_ORDERBOOK_DIFF_2021_09.csv", header=False, index=False, mode="a")

def get_json_obj(datas):
    js = {}
    for (price, size) in datas:
        if size < 1e-4:
            size = format(size, '.8f')
        if price in js:
            js[price] += size
        else:
            js[price] = size
    return js


def raw_data_df(asks, bids, times):
    datas = []
    for i in range(len(asks)):
        asks_json = get_json_obj(asks[i])
        bids_json = get_json_obj(bids[i])
        data = {"asks":asks_json, "bids":bids_json}
        datas.append(json.dumps(data))
    df = pd.DataFrame({"timestamp":times,"data":datas})
    #print("... Write into csv file ...")
    #df.to_csv("BTCUSDT_SPOT_ORDERBOOK_DIFF_2021_09.csv", header=False, index=False, mode="a")
    sql = "INSERT INTO ORDERBOOK_200 (timestamp, data) VALUES ( '{times}', '{datas}');".format(times=times,datas=datas )    
            cur.execute(sql)
            mydb.commit()
    print("... Write into sql file ...")
'''
def to_csv_10(asks, bids, time):
    print("... Write into csv file ...")
    asks_json = get_json_obj(asks)
    bids_json = get_json_obj(bids)
    data = {"asks":asks_json, "bids":bids_json}
    df = pd.DataFrame({"timestamp":[time],
                    "data":[json.dumps(data)]})
    df.to_csv("BTCUSDT_SPOT_ORDERBOOK_FULL_2021_09.csv", header=False, index=False, mode="a")
    '''
'''
def init():
    data = {'timestamp': [], 'data':[]}
    res = pd.DataFrame(data)
    res.to_csv("BTCUSDT_SPOT_ORDERBOOK_DIFF_2021_09.csv", header=True, index=False, mode="a")
    
    # for seperating the asks/bids columns
    # res = pd.concat([get_lists([[]], [[]], "asks"), get_lists([[]], [[]], "bids")], axis=1)
    # res.to_csv("orderbook.csv", header=True, index=False, mode="w")
    
def init_interval():
    data = {'timestamp': [], 'data':[]}
    res_10 = pd.DataFrame(data)
    res_10.to_csv("BTCUSDT_SPOT_ORDERBOOK_FULL_2021_09.csv", header=True, index=False, mode="a")
'''
def write(csv_asks, cvs_bids, csv_since):
    t = threading.Thread(target = raw_data_df,  args=[csv_asks, cvs_bids, csv_since])
    t.start()
def write_interval(csv_asks, cvs_bids, csv_since):
    t2 = threading.Thread(target = to_csv_10,  args=[csv_asks[0], cvs_bids[0], csv_since[0]])
    t2.start()





    
