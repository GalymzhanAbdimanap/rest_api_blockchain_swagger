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
SMART_CONTRACT_ADDRESS = '419772BA0D80F691959BAC413FAEDBC44C7FEE8536'
DEFAULT_ADDRESS = '41FCF23797364C955A23B73F711219FBF5564B2C17'


TOKEN_CONTRACT = '411576d1a39ace4f0a24fc52b7a17be97904f6a2b8'
ADDRESS_STORE = '418C7AFBB25E62271699A1254CFAAF4DAA427D1932' # Seller.

TOKEN_CREATOR = "41FCF23797364C955A23B73F711219FBF5564B2C17"
TOKEN_CREATOR_PRIVATE_KEY = "464d87c77a61a1065e3d21e6e6be9cd3aaeb0ce59724a77c5e86cbeed38bd9b7"
                              
#------------------------------------------------------------------------------
# Addresses of contract which we use.
#------------------------------------------------------------------------------

# token contract - 411576d1a39ace4f0a24fc52b7a17be97904f6a2b8
# old marketplace contract - 41157290966C5D65633276C184D110E4C1DC96C577
# new marketplace contract - TPmzUP412cPUHZXeSqrBJGxZXywoYcEf7c  // 419772BA0D80F691959BAC413FAEDBC44C7FEE8536

#------------------------------------------------------------------------------


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


def getTokens_utils(account_address, value=30000000000):
    """User get tokens on value 300."""
    e = {'txid':'Error!'} 
    logsOfError = ''
    try:
        trigger = tron.transaction_builder.trigger_smart_contract(contract_address = TOKEN_CONTRACT,
                                function_selector = 'transfer(address,uint256)', #без пробелов!
                                fee_limit=1000000000,
                                call_value=0,
                                parameters=[{'type':'address','value':account_address},{'type': 'int256','value':value}],
                                issuer_address=TOKEN_CREATOR
                                )

        tron.private_key = TOKEN_CREATOR_PRIVATE_KEY
        transaction = trigger['transaction']
        signed1_tx = tron.trx.sign(transaction,True,False)
        e = tron.trx.broadcast(signed1_tx)
    except Exception as ex:
        logsOfError = logsOfError + str(ex)
    return {'txID':e['txid'], 'logs':logsOfError}


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
