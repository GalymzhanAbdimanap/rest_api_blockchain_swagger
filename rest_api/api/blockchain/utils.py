#!flask/bin/python
"""
Blockchain API
Api for connecting blockchain technology with a mobile application.
Blockchain: TRON;

Copyright (c) 2020 IDET.kz
Written by Galymzhan Abdymanap.
Version 1.0
"""

#-------------------------------------------------------------------------------
# Import blockchain API library and TRON (blockchain) init
#-------------------------------------------------------------------------------
from tronapi import Tron
from tronapi import HttpProvider
from trx_utils import decode_hex
from eth_abi import decode_abi
full_node = HttpProvider('https://api.shasta.trongrid.io')
solidity_node = HttpProvider('https://api.shasta.trongrid.io')
event_server = HttpProvider('https://api.shasta.trongrid.io')

tron = Tron(full_node=full_node,
        solidity_node=solidity_node,
        event_server=event_server)

#--------------------------------------------------------------------------------
# Smart contract address and default user address on Blockchain
SMART_CONTRACT_ADDRESS = '41157290966C5D65633276C184D110E4C1DC96C577'
DEFAULT_ADDRESS = '41FCF23797364C955A23B73F711219FBF5564B2C17'




def getIndexOfGoods():
    """Return last index of goods on blockchain Market."""

    a = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                               function_selector = 'getIndexAuctions()',
                               fee_limit=1000000000,
                               call_value=0,
                               parameters=[],
                               issuer_address=DEFAULT_ADDRESS
                               )
    a = a['constant_result']
    decodeH = decode_hex(a[0])
    decodeA= decode_abi(('uint256',),decodeH)
    print(decodeA[0])
    return decodeA[0]


def getIndexOfChecks(account_address):
    """Return all checks index of user."""

    a = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                               function_selector = 'getIndexOfChecksAndIsConfirm(address)',
                               fee_limit=1000000000,
                               call_value=0,
                               parameters=[{'type': 'address', 'value': account_address}],
                               issuer_address=account_address
                               )
    a = a['constant_result']
    decodeH = decode_hex(a[0])
    decodeA= decode_abi(('uint256[]',),decodeH)
    print(decodeA[0])
    return decodeA[0]


def createAccount_blockchain():
    """Return new account on blockchain."""

    logsOfError=''
    try:
        account = tron.create_account
    except Exception as e:
        logsOfError = logsOfError+str(e)
    return {'publicKey':str(account.public_key), 'base58':str(account.address.base58), 'hex':str( account.address.hex), 'privateKey':str(account.private_key), 'logs':logsOfError, 'status':'success'}


def getAddressOfgoods(account_address):
    """Return index of goods from wallet of user."""

    addresses = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                               function_selector = 'getAddressOfGoodFromWallet(address)',
                               fee_limit=1000000000,
                               call_value=0,
                               parameters=[{'type': 'address', 'value':account_address}],
                               issuer_address=account_address
                               )
    addresses = addresses['constant_result']
    decodeH = decode_hex(addresses[0])
    decodeA= decode_abi(('uint256[]',),decodeH)
    print("----------------------------------------------------")
    print(decodeA)
    return decodeA[0]


