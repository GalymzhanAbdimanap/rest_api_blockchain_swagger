import logging

from flask import request
from flask_restplus import Resource
from rest_api.api.blockchain.utils import smart_contract_address, default_address
from rest_api.api.blockchain.serializers import purchaseGoods, confirmGoods, saleOfGoods, cancelOfPurchase, freeze_balance, unfreeze_balance
#from rest_api_demo.api.blog.parsers import pagination_arguments
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

ns = api.namespace('payable/', description='Operations that require a private key')


@ns.route('/purchaseGoods')
class purchaseGoods(Resource):

    
    @api.expect(purchaseGoods)
    def post(self):
        """
        
        """
        id_goods =[]
        amounts_goods=[]
        logsOfError=''
        

        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        amounts_goods = data['amounts_goods']
        timestamp = data['timestamp']
        
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'placeBidBox(uint256[],uint256[],string)', #без пробелов!
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type':'int256[]','value':id_goods},{'type': 'int256[]','value':amounts_goods},{'type':'string','value':timestamp}],
                                    issuer_address=account_address
                                    )

            tron.private_key = private_key
            transaction = trigger['transaction']
            signed1_tx = tron.trx.sign(transaction,True,False)
            e = tron.trx.broadcast(signed1_tx)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'txID':e['txid'], 'logs':logsOfError}


@ns.route('/confirmGoods')
class confirmGoods(Resource):

    
    @api.expect(confirmGoods)
    def post(self):
        """
        
        """
        id_goods=[]
        logsOfError=''

        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        id_check = data['id_check']
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'finalizeBox(uint256[],uint256)', #без пробелов!
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type':'int256[]','value':id_goods},{'type': 'int256','value':id_check}],
                                    issuer_address=account_address
                                    )

            tron.private_key = private_key
            transaction = trigger['transaction']
            signed1_tx = tron.trx.sign(transaction,True,False)
            e = tron.trx.broadcast(signed1_tx)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'txID':e['txid'], 'logs':logsOfError}

@ns.route('/saleOfGoods')
class saleOfGoods(Resource):

    
    @api.expect(saleOfGoods)
    def post(self):
        """
        
        """
        amounts=[]
        id_goods=[]
        logsOfError=''

        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        amounts = data['amounts_goods']
        timestamp = data['timestamp']
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'saleOfGoodsBox(uint256[],uint256[],string)', #без пробелов!
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type':'int256[]','value':amounts},{'type': 'int256[]','value':id_goods},{'type': 'string','value':timestamp}],
                                    issuer_address=account_address
                                    )

            tron.private_key = private_key
            transaction = trigger['transaction']
            signed1_tx = tron.trx.sign(transaction,True,False)
            e = tron.trx.broadcast(signed1_tx)
        except Exception as e:
            logsOfError = logsOfError +str(e)
        return {'txID':e['txid'], 'logs': logsOfError}

@ns.route('/cancelOfPurchase')
class cancelOfPurchase(Resource):

    
    @api.expect(cancelOfPurchase)
    def post(self):
        """
        
        """
        id_goods=[]
        logsOfError=''

        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        id_check = data['id_check']
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = smart_contract_address,
                                    function_selector = 'cancelConfirmBox(uint256[],uint256)', #без пробелов!
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type':'int256[]','value':id_goods},{'type': 'int256','value':id_check}],
                                    issuer_address=account_address
                                    )

            tron.private_key = private_key
            transaction = trigger['transaction']
            signed1_tx = tron.trx.sign(transaction,True,False)
            e = tron.trx.broadcast(signed1_tx)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'txID':e['txid'], 'logs':logsOfError}


@ns.route('/freeze_balance')
class freeze_balance(Resource):

    
    @api.expect(freeze_balance)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key = data['privateKey']
        amount = data['amount']
        resource = data['resource'] #bandwith or energy


        try:
            tron.private_key = private_key
            freeze_balance = tron.trx.freeze_balance(amount = amount, resource=resource, account = account_address)
            print(freeze_balance)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'txid':str(freeze_balance['txid']), 'logs':logsOfError}


@ns.route('/unfreeze_balance')
class unfreeze_balance(Resource):

    
    @api.expect(unfreeze_balance)
    def post(self):
        """
        
        """
        logsOfError=''
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key = data['privateKey']
        resource = data['resource'] #bandwith or energy


        try:
            tron.private_key = private_key
            unfreeze_balance = tron.trx.unfreeze_balance(resource=resource, account = account_address)
            print(unfreeze_balance)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'unfreeze_balance':str(unfreeze_balance), 'logs':logsOfError}

