import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
#from flask_jsonrpc.proxy import ServiceProxy

rpc_username = 'rpdasplatinum'
rpc_password = '1bcd3c84c84f87eaa86e4e56834c92927a07f9e'
rpc_ip = '127.0.0.1'
rpc_port = 54582


#Make rpc connection with DGB core
def ServiceProxy():
    return AuthServiceProxy('http://%s:%s@%s:%i'%(rpc_username, rpc_password, rpc_ip, rpc_port))

rpc_connection = ServiceProxy()


def validateAddress(address):
    rpc_connection = ServiceProxy()
    validate = rpc_connection.validateaddress(address)
    return validate['isvalid']

def getAddress(account):
    rpc_connection = ServiceProxy()
    account = rpc_connection.getaccountaddress(account)
    print(account)

    print(account)
    return account

def getBalance(account,minconf=1):
    rpc_connection = ServiceProxy()
    try:
        balance = rpc_connection.getbalance(account,minconf)
    except ValueError:
        balance = -1
    return balance

def withdraw(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        return rpc_connection.sendfrom(account,destination,amount)

def tip(account,destination,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        rpc_connection.move(account,destination,amount)

def rain(account,amount):
    if amount > getBalance(account) or amount <= 0:
        raise ValueError("Invalid amount.")
    else:
        rpc_connection = ServiceProxy()
        accounts = rpc_connection.listaccounts()
        #amount = 1
        eachTip = amount / len(accounts)
        for ac in accounts:
            tip(account,ac,eachTip)
        return eachTip

#API commands
def getPrice():
    edcashCapJson = requests.get('https://api.coingecko.com/api/v3/coins/dash-platinum').json()
    mk_cap = edcashCapJson ['market_data']['market_cap']['usd']
    pricebrl = edcashCapJson ['market_data']['current_price']['brl']
    priceusd = edcashCapJson ['market_data']['current_price']['usd']
    pricebtc = edcashCapJson ['market_data']['current_price']['btc']
    priceeth = edcashCapJson ['market_data']['current_price']['eth']

    return pricebrl, priceusd, pricebtc, priceeth, mk_cap

def getPriceMSG():

    pricebrl, priceusd, pricebtc, priceeth, mk_cap = getPrice()

    msg = "\nDashp Price:\n```Market Cap: ${:.3f}```".format(float(mk_cap))+ "\n```Price(BRL):  R${:.8f}```".format(pricebrl) + "\n```Price(USD):  ${:.8f}```".format(priceusd) + "\n```Price(BTC):  {:.8f}```".format(pricebtc) + "\n```Price(ETH):  {:.8f}```".format(priceeth)
    return msg

