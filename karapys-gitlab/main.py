import os
from web3 import Web3

RPC_URL = os.environ['RPC_URL']

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def sendTx():
    sender = web3.eth.coinbase
    web3.personal.unlockAccount(sender, '')
    web3.eth.sendTransaction({
        'from': sender,
        'to': '0x0000000000000000000000000000000000000000',
        'value': 100
    })