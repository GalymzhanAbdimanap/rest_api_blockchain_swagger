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

smart_contract_address = '41157290966C5D65633276C184D110E4C1DC96C577'
default_address = '41FCF23797364C955A23B73F711219FBF5564B2C17'




def getIndexOfGoods():
    a = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                               function_selector = 'getIndexAuctions()',
                               fee_limit=1000000000,
                               call_value=0,
                               parameters=[],
                               issuer_address=default_address
                               )
    a = a['constant_result']
    decodeH = decode_hex(a[0])
    decodeA= decode_abi(('uint256',),decodeH)
    print(decodeA[0])
    return decodeA[0]


def getIndexOfChecks(account_address):
    a = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
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

def getAddressOfgoods(account_address):
    addresses = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
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
