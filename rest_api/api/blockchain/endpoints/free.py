import logging

from flask import request
from flask_restplus import Resource
from rest_api.api.blockchain.utils import getIndexOfGoods, getIndexOfChecks, getAddressOfgoods, smart_contract_address, default_address
from rest_api.api.blockchain.serializers import getChecks, getWallet, balanceOfToken, balanceOfTrx
from rest_api.api.restplus import api




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
#smart_contract_address = '41157290966C5D65633276C184D110E4C1DC96C577'
#default_address = '41FCF23797364C955A23B73F711219FBF5564B2C17'




log = logging.getLogger(__name__)

ns = api.namespace('free/', description='Operations that do not require a private key')


@ns.route('/getGoods')
class getGoods(Resource):

    
    #@api.response(201, 'Category successfully created.')
    #@api.expect(getGoods)
    def post(self):
        """
        
        """
        logsOfError=''
        contents=[]
        try:
            indexOfGoods = getIndexOfGoods()
            for i in range(0, indexOfGoods):
                returnContent = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'returnContentsAuctions(uint256)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[ {'type': 'int256', 'value': i}],
                                    issuer_address=default_address
                                    )
                returnContent = returnContent['constant_result']
                decodeH = decode_hex(returnContent[0])
                decodeA= decode_abi(('uint256', 'string', 'uint256', 'string', 'uint256', 'uint256',),decodeH)
                res_data = {"id_goods":decodeA[0], "title":decodeA[1], "price":decodeA[2], "description":decodeA[3], "count":decodeA[4], "commision":decodeA[5]}
                contents.append(res_data)
                print(decodeA)
        except Exception as e:
            logsOfError=logsOfError + str(e)

        return {'goods': contents, 'logs':logsOfError}


@ns.route('/getChecks')
class getChecks(Resource):

    @api.expect(getChecks)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']

        indexOfChecks = []
        checks=[]
        try:
            indexOfChecks = getIndexOfChecks(account_address)
            for i in indexOfChecks:
                check = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'getChecksOfGoods(address,uint256)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type': 'address', 'value':account_address},{'type': 'int256', 'value': i}],
                                    issuer_address=account_address
                                    )
                check = check['constant_result']
                decodeH = decode_hex(check[0])
                decodeA= decode_abi(('string[]','uint256[]','uint256[]','uint256[]','address[]','uint256','string','bool','uint256','string','bool',),decodeH)
                print(decodeA)
                res_data = {"nameOfGood":decodeA[0], "amountOfgood":decodeA[1], "price":decodeA[2], "sumPrice":decodeA[3], "addressOfContract":decodeA[4], "id_check":decodeA[5] ,"timestamp":decodeA[6], "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                checks.append(res_data)
                #print(decodeA)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'checks': checks, 'logs':logsOfError}


@ns.route('/getWallet')
class getWallet(Resource):

    @api.expect(getWallet)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']

        good_addresses = []
        wallets=[]
        try:
            good_addresses = getAddressOfgoods(account_address)
            for i in good_addresses:
                wallet = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'getWalletOfGood_array(address,uint256)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type': 'address', 'value':account_address},{'type': 'int256', 'value':i}],
                                    issuer_address=account_address
                                    )
                wallet = wallet['constant_result']
                decodeH = decode_hex(wallet[0])
                decodeA= decode_abi(('string','uint256','uint256','uint256','uint256',),decodeH)
                res_data = {"nameOfGood":decodeA[0], "amountOfGood":decodeA[1], "price":decodeA[2], "addressOfGood":decodeA[3], "commission":decodeA[4]}
                wallets.append(res_data)
                #print(decodeA)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'wallets': wallets, 'logs':logsOfError}


@ns.route('/balanceOfToken')
class balanceOfToken(Resource):

    @api.expect(balanceOfToken)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']

        try:
            balance = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'balanceOf(address)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type': 'address', 'value':account_address}],
                                    issuer_address=account_address
                                    )
            balance = balance['constant_result']
            decodeH = decode_hex(balance[0])
            decodeA= decode_abi(('uint256',),decodeH)
            print("----------------------------------------------------")
            print(decodeA)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'balance':str(decodeA[0]/100000000), 'logs':logsOfError}


@ns.route('/balanceOfTrx')
class balanceOfTrx(Resource):

    @api.expect(balanceOfTrx)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']

        try:
            balance = tron.trx.get_balance(account_address, is_float=True)
            print(balance)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'balanceTrx':str(balance), 'logs':logsOfError}


@ns.route('/create_account')
class create_account(Resource):

    def post(self):
        """
        
        """
        logsOfError=''

        try:
            
            account = tron.create_account
            print(account)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'publicKey':str(account.public_key), 'base58':str(account.address.base58), 'hex':str( account.address.hex), 'privateKey':str(account.private_key), 'logs':logsOfError}

