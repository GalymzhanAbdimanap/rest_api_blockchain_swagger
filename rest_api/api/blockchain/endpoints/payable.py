#!flask/bin/python
"""
Blockchain API
Api for connecting blockchain technology with a mobile application.
Blockchain: TRON;

Copyright (c) 2020 IDET.kz
Written by Galymzhan Abdymanap.
Version 1.0
"""

import logging

from flask import request
from flask_restplus import Resource
from datetime import datetime

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)


#-----------------------------------------------------------------------------------
# Import blockchain API library and blockchain init
#-----------------------------------------------------------------------------------
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
# SMART_CONTRACT_ADDRESS = '41157290966C5D65633276C184D110E4C1DC96C577'
# DEFAULT_ADDRESS = '41FCF23797364C955A23B73F711219FBF5564B2C17'

# Import support modules from this project
from rest_api.api.blockchain.utils import SMART_CONTRACT_ADDRESS, DEFAULT_ADDRESS
from rest_api.api.blockchain.serializers import purchaseGoods, confirmGoods, saleOfGoods, cancelOfPurchase, freeze_balance, unfreeze_balance
from rest_api.api.restplus import api

# Create logger
log = logging.getLogger(__name__)

ns = api.namespace('payable/', description='Operations that require a private key')

@ns.route('/purchaseGoods')
class purchaseGoods(Resource):
    """Allows to shop for goods on blockchain Market. Return hash address of transaction."""
    @jwt_required
    @api.expect(purchaseGoods)
    def post(self):
        """Allows to shop for goods on blockchain Market. Return hash address of transaction."""

        id_goods =[]
        amounts_goods=[]
        logsOfError=''
        # Input data
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        amounts_goods = data['amounts_goods']
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                                    function_selector = 'placeBidBox(uint256[],uint256[],string)', # Without space / без пробелов!
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
    """Allows to confirm shop for goods on blockchain Market. Return hash address of transaction."""

    @jwt_required
    @api.expect(confirmGoods)
    def post(self):
        """Allows to confirm shop for goods on blockchain Market. Return hash address of transaction."""

        id_goods=[]
        logsOfError=''
        # Input data
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        id_check = data['id_check']
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
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
    """Allows the sale of goods that the user has on the Blockchain Market. Return hash address of transaction.
    For work this function, in smart contract(MarketPlace) must have TOKENS."""

    @jwt_required
    @api.expect(saleOfGoods)
    def post(self):
        """Allows the sale of goods that the user has on the Blockchain Market. Return hash address of transaction."""

        amounts=[]
        id_goods=[]
        logsOfError=''
        # Input data
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        amounts = data['amounts_goods']

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
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
    """Allows to cancel a purchase that has not yet been confirmed on the Blockchain Market.
    Return hash address of transaction."""

    @jwt_required
    @api.expect(cancelOfPurchase)
    def post(self):
        """Allows to cancel a purchase that has not yet been confirmed on the Blockchain Market. 
        Return hash address of transaction."""

        id_goods=[]
        logsOfError=''
        # Input data
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key =  data['privateKey']
        id_goods = data['id_goods']
        id_check = data['id_check']
        
        try:
            trigger = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
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
    """Allows to freeze balance to give ENERGY or BANDWIDTH on the Blockchain. Return hash address of transaction."""

    @jwt_required
    @api.expect(freeze_balance)
    def post(self):
        """Allows to freeze balance to give ENERGY or BANDWIDTH on the Blockchain. Return hash address of transaction."""

        logsOfError=''
        # Input data
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
    """Allows to unfreeze balance on the Blockchain. Return hash address of transaction."""

    @jwt_required
    @api.expect(unfreeze_balance)
    def post(self):
        """Allows to unfreeze balance on the Blockchain. Return hash address of transaction."""

        logsOfError=''

        # Input data
        data = request.get_json(force=True)
        account_address =  data['account_address']
        private_key = data['privateKey']
        resource = data['resource'] # bandwith or energy


        try:
            tron.private_key = private_key
            unfreeze_balance = tron.trx.unfreeze_balance(resource=resource, account = account_address)
            print(unfreeze_balance)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'unfreeze_balance':str(unfreeze_balance), 'logs':logsOfError}

