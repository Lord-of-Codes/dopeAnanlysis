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
    if MARKETS[I]['BaseVolume'] > 0.50 or MARKETS[I]['BaseVolume'] < 0.01 :
        MARKETS.pop(I) #Not time efficient. But whatever. Will fix it later.
    else:
        I = I + 1

J = 0
while J < len(MARKETS):
	ORDERS, ERROR = API.get_orders(str(MARKETS[J]['TradePairId']))
	if ERROR is not None:
		print (ERROR)
	K = 0
	SUMBTC = 0
	FIRSTSELL = ORDERS['Sell'][0]['Price']
	while K < 50:
		if ORDERS['Sell'][K]['Total'] > 0.1:
			MARKETS.pop(J)
			break
		SUMBTC = SUMBTC + ORDERS['Sell'][K]['Total']
		if SUMBTC > 1:
			if ORDERS['Sell'][K]['Price'] < FIRSTSELL*1.8:
				MARKETS.pop(J)
				break
		K=K+1
print (len(MARKETS))
