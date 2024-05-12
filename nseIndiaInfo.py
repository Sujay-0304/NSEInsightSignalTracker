import requests
import pandas as pd
import time

index_symbols = {
    '1': 'NIFTY',
    '2': 'BANKNIFTY',
    '3': 'FINNIFTY',
    # '4': 'SENSEX',
} 
print("Select the index to get the data\n 1. NIFTY\n 2. BANKNIFTY\n 3. FINNIFTY\n")
index = input("Enter the index number: ").strip()
print("You have selected: ", index_symbols[index]+"\n")


url = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + index_symbols[index]
# url = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37','accept-encoding': 'gzip, deflate, br','accept-language': 'en-GB,en;q=0.9,en-US;q=0.8'}

session = requests.Session()
request = session.get(url,headers=header)
cookies = dict(request.cookies)

# initialize the url and headers
response = session.get(url,headers=header,cookies=cookies).json()
rawdata = pd.DataFrame(response)

# get the required data from the response
current_value = rawdata['records']['underlyingValue']
time_stamp = rawdata['records']['timestamp'] 

# get the data from the response
def dataframe():
    response = session.get(url,headers=header,cookies=cookies).json()
    rawdata = pd.DataFrame(response)
    rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)

    data = []
    for i in range(0,len(rawop)):
        calloi = callcoi = cltp = putoi = putcoi = pltp = 0
        stp = rawop['strikePrice'][i]
        if(rawop['CE'][i]==0):
            calloi = callcoi = 0
        else:
            calloi = rawop['CE'][i]['openInterest']
            callcoi = rawop['CE'][i]['changeinOpenInterest']
            cltp = rawop['CE'][i]['lastPrice']
        if(rawop['PE'][i] == 0):
            putoi = putcoi = 0
        else:
            putoi = rawop['PE'][i]['openInterest']
            putcoi = rawop['PE'][i]['changeinOpenInterest']
            pltp = rawop['PE'][i]['lastPrice']
        opdata = {
            'CALL OI': calloi, 'CALL CHNG OI': callcoi, 'CALL LTP': cltp, 'STRIKE PRICE': stp,
            'PUT OI': putoi, 'PUT CHNG OI': putcoi, 'PUT LTP': pltp
        }
        
        data.append(opdata)
    # print("Data Fetched Successfully") 
    optionchain = pd.DataFrame(data)
    return optionchain

# def change_in_oi():
#     print(dataframe())
#     current_value = rawdata['records']['underlyingValue'] 

# change_in_oi() 

while True:
    optionchain = dataframe()

    total_call_oi = optionchain['CALL OI'].sum()
    total_put_oi = optionchain['PUT OI'].sum() 
    difference_in_oi = total_call_oi - total_put_oi 
    if time_stamp == rawdata['records']['timestamp']:
        print(time_stamp)
        time_stamp = rawdata['records']['timestamp']
        print("total call oi =", total_call_oi)
        print("total put oi =", total_put_oi) 
        print("difference in oi =", difference_in_oi) 

        if difference_in_oi >= 2000000:
            print("strong Bearish: ",difference_in_oi)
        elif difference_in_oi <= -2000000:
            print("strong Bullish: ",difference_in_oi)
        elif difference_in_oi >= 1500000:
            print("Mild Bearish: ",difference_in_oi)
        elif difference_in_oi <= -1500000:
            print("Mild Bullish: ",difference_in_oi) 
        else:
            print("Neutral conseldate market: ",difference_in_oi)
        print("--------------------------------------------")
    # time.sleep(10)



