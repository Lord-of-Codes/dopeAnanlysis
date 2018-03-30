import signal
import sys
import json
from cryptopia_api import Api

def get_secret(secret_file):
    """Grabs API key and secret from file and returns them"""

    with open(secret_file) as secrets:
        secrets_json = json.load(secrets)
        secrets.close()

    return str(secrets_json['key']), str(secrets_json['secret'])

def sigint_handler():
    """Handler for ctrl+c"""
    print ('\n[!] CTRL+C pressed. Exiting...')
    sys.exit(0)

KEY, SECRET = get_secret("secrets.json")
API = Api(KEY, SECRET)

signal.signal(signal.SIGINT, sigint_handler)
print ('\nWelcome to dopeAnalysis')

MARKETS, ERROR = API.get_markets('BTC')
if ERROR is not None:
    print (ERROR)

I = 0
while I < len(MARKETS):
    if MARKETS[I]['BaseVolume'] > 0.50 or MARKETS[I]['BaseVolume'] < 0.01 :  #Selecting coins whose daily trade volume is between 0.01 btc to 0.5 btc
        del MARKETS[I] #Not time efficient. But whatever. Will fix it later.
    else:
        I = I + 1  #Since the (I+1)th index is not moving to (I)th place. Therefore, incrementing I

J = 0
while J < len(MARKETS):
	ORDERS, ERROR = API.get_orders(str(MARKETS[J]['TradePairId'])) 	#Fetching market orders using TradePair Id of the coins who remain in list after above loop
	if ERROR is not None:
		print (ERROR)
	K = 0		
	SUMBTC = 0.0		#To count the total sum of sell orders on moving down the sell orders list
	FIRSTSELL = ORDERS['Sell'][0]['Price']		#Ask Price. Lowest Price at which a seller is willing to sell.
	FLAG = 0
	while K < 100:		
		if ORDERS['Sell'][K]['Total'] > 0.1:		#Checking for sell walls
			del MARKETS[J]
			FLAG = 1
			break
		SUMBTC = SUMBTC + ORDERS['Sell'][K]['Total']	#Calculating total sum
		if SUMBTC > 0.5:
			if ORDERS['Sell'][K]['Price'] < FIRSTSELL*1.8:		#checking if the price of coin rises by 40% on investment of 0.5btc
				del MARKETS[J]
				FLAG = 1
			break
		K=K+1		
	if FLAG == 0:
		J=J+1		#same concept as in line 35
print (len(MARKETS))
