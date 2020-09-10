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
from flask_bcrypt import Bcrypt
import sqlite3 

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail


# Import library for use blockchain
from tronapi import Tron
from tronapi import HttpProvider
from trx_utils import decode_hex
from eth_abi import decode_abi

#------------------------------------------------------------------------
# TRON (blockchain) init
#------------------------------------------------------------------------
full_node = HttpProvider('https://api.shasta.trongrid.io')
solidity_node = HttpProvider('https://api.shasta.trongrid.io')
event_server = HttpProvider('https://api.shasta.trongrid.io')
tron = Tron(full_node=full_node,
        solidity_node=solidity_node,
        event_server=event_server)

#SMART_CONTRACT_ADDRESS = '41157290966C5D65633276C184D110E4C1DC96C577'
#DEFAULT_ADDRESS = '41FCF23797364C955A23B73F711219FBF5564B2C17'

# Import support modules from this project
from rest_api.api.blockchain.utils import getIndexOfGoods, getIndexOfChecks, getAddressOfgoods, SMART_CONTRACT_ADDRESS, DEFAULT_ADDRESS, createAccount_blockchain, getTokens_utils
from rest_api.api.blockchain.serializers import getChecks, getWallet, balanceOfToken, balanceOfTrx, registration, oauth
from rest_api.api.restplus import api
from rest_api.api.blockchain.endpoints.oauth import createToken, auth, verify_token
from rest_api import settings


ACCESS_TOKEN_EXPIRES_IN=900
API_EMAIL_CONFIRM_ADDRESS = 'http://82.200.167.74:8837/api/free/oauth/confirm_email/'

# 
connection = sqlite3.connect('rest_api/database/Users.db',check_same_thread=False)

# Create logger
log = logging.getLogger(__name__)

#---------------------------------------------------------------------------------------------------------------

ns = api.namespace('free/', description='Operations that do not require a private key')

@ns.route('/getGoods')
class getGoods(Resource):
    """Return all goods from blochain Market."""
    
    @jwt_required
    def get(self):
        """Return all goods from blochain Market."""

        logsOfError=''
        contents=[]
        try:
            indexOfGoods = getIndexOfGoods()
            for i in range(0, indexOfGoods):
                returnContent = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                                    function_selector = 'returnContentsAuctions(uint256)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[ {'type': 'int256', 'value': i}],
                                    issuer_address=DEFAULT_ADDRESS
                                    )
                returnContent = returnContent['constant_result']
                decodeH = decode_hex(returnContent[0])
                decodeA= decode_abi(('uint256', 'string', 'uint256', 'string', 'uint256', 'uint256',),decodeH)
                res_data = {"id_good":decodeA[0], "nameOfGood":decodeA[1], "price":decodeA[2], "description":decodeA[3], "amountOfGood":decodeA[4], "commision":decodeA[5]}
                contents.append(res_data)
                print(decodeA)
        except Exception as e:
            logsOfError=logsOfError + str(e)

        return {'data': contents, 'logs':logsOfError}


@ns.route('/getChecks/<account_address>/<typeOfOp>')
class getChecks(Resource):
    """Return all checks of users from blochain Market."""
    
    @jwt_required
    def get(self, account_address, typeOfOp=None):
        """Return all checks of users from blochain Market."""

        logsOfError=''
        indexOfChecks = []
        checks=[]
        
        try:
            # If type operation don`t select then return checks of all type operations 
            if typeOfOp==None:
                indexOfChecks = getIndexOfChecks(account_address)
                for i in indexOfChecks:
                    check = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                                        function_selector = 'getChecksOfGoods(address,uint256)',
                                        fee_limit=1000000000,
                                        call_value=0,
                                        parameters=[{'type': 'address', 'value':account_address},{'type': 'int256', 'value': i}],
                                        issuer_address=account_address
                                        )
                    check = check['constant_result']
                    decodeH = decode_hex(check[0])
                    decodeA= decode_abi(('string[]','uint256[]','uint256[]','uint256[]','uint256[]','uint256','string','bool','uint256','string','bool',),decodeH)
                    print(decodeA)
                    #res_data = {"nameOfGood":decodeA[0], "amountOfgood":decodeA[1], "price":decodeA[2], "sumPrice":decodeA[3], "addressOfContract":decodeA[4], "id_check":decodeA[5] ,"timestamp":decodeA[6], "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                    addressOfContract = decodeA[4]
                    #print(len(addressOfContract))
                    goods=[]
                    for i in range(len(addressOfContract)):
                        good_data = {"nameOfGood":decodeA[0][i], "amountOfGood":decodeA[1][i], "price":decodeA[2][i], "sumPrice":decodeA[3][i], "addressOfContract":decodeA[4][i]}
                        goods.append(good_data)
                    if len(decodeA[6]) < 6:
                        print("timestamp")
                        timestamp = "2020-06-12T11:41:19"
                    else:
                        timestamp = decodeA[6]
                    #res_data = {"goods":goods, "id_check":decodeA[5], "timestamp":decodeA[6], "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                    res_data = {"goods":goods, "id_check":decodeA[5], "timestamp":timestamp, "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                    checks.append(res_data)


                    #print(decodeA)
            else:
                indexOfChecks = getIndexOfChecks(account_address)
                for i in indexOfChecks:
                    check = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                                        function_selector = 'getChecksOfGoods(address,uint256)',
                                        fee_limit=1000000000,
                                        call_value=0,
                                        parameters=[{'type': 'address', 'value':account_address},{'type': 'int256', 'value': i}],
                                        issuer_address=account_address
                                        )
                    check = check['constant_result']
                    decodeH = decode_hex(check[0])
                    decodeA= decode_abi(('string[]','uint256[]','uint256[]','uint256[]','uint256[]','uint256','string','bool','uint256','string','bool',),decodeH)
                    print(decodeA)
                    #res_data = {"nameOfGood":decodeA[0], "amountOfgood":decodeA[1], "price":decodeA[2], "sumPrice":decodeA[3], "addressOfContract":decodeA[4], "id_check":decodeA[5] ,"timestamp":decodeA[$
                    addressOfContract = decodeA[4]
                    #print(len(addressOfContract))
                    goods=[]
                    for i in range(len(addressOfContract)):
                        good_data = {"nameOfGood":decodeA[0][i], "amountOfGood":decodeA[1][i], "price":decodeA[2][i], "sumPrice":decodeA[3][i], "addressOfContract":str(decodeA[4][i]), "id_good":decodeA[4][i]}
                        goods.append(good_data)
                    # timestamp = decodeA[6]
                    # Test. On production delete if and else
                    if len(decodeA[6]) < 6:
                        print("timestamp")
                        timestamp = "2020-06-12T11:41:19"
                    else:
                        timestamp = decodeA[6]
                
                    #res_data = {"goods":goods, "id_check":decodeA[5], "timestamp":decodeA[6], "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                    res_data = {"goods":goods, "id_check":decodeA[5], "timestamp":timestamp, "status":decodeA[7], "allSumPrice":decodeA[8], "typeOfOp":decodeA[9], "isCanceled":decodeA[10]}
                    
                    if typeOfOp==decodeA[9]:
                        checks.append(res_data)


                    #print(decodeA)
   
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'data': checks, 'logs':logsOfError}


@ns.route('/getWallet/<account_address>')
class getWallet(Resource):
    """Return all goods which user have."""
    
    @jwt_required
    def get(self, account_address):
        """Return all goods which user have."""

        logsOfError=''
        good_addresses = []
        wallets=[]
        try:
            good_addresses = set(getAddressOfgoods(account_address))
            for i in good_addresses:
                wallet = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
                                    function_selector = 'getWalletOfGood_array(address,uint256)',
                                    fee_limit=1000000000,
                                    call_value=0,
                                    parameters=[{'type': 'address', 'value':account_address},{'type': 'int256', 'value':i}],
                                    issuer_address=account_address
                                    )
                wallet = wallet['constant_result']
                decodeH = decode_hex(wallet[0])
                decodeA= decode_abi(('string','uint256','uint256','uint256','uint256',),decodeH)
                res_data = {"nameOfGood":decodeA[0], "amountOfGood":decodeA[1], "price":decodeA[2], "id_good":decodeA[3], "commission":decodeA[4]}
                wallets.append(res_data)
                #print(decodeA)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'data': wallets, 'logs':logsOfError}


@ns.route('/balance/<account_address>')
class balanceOfToken(Resource):
    """Return balance of IdetToken and TRX."""
    
    @jwt_required
    def get(self, account_address):
        """Return balance of IdetToken and TRX."""

        logsOfError=''
        try:
            balance = tron.transaction_builder.trigger_smart_contract(contract_address = SMART_CONTRACT_ADDRESS,
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
            balanceTrx = tron.trx.get_balance(account_address, is_float=True)
        except Exception as e:
            logsOfError = logsOfError + str(e)
        return {'balanceOfToken':str(decodeA[0]/100000000), 'balanceTrx':str(balanceTrx), 'logs':logsOfError}


@ns.route('/balanceOfTrx/<account_address>')
class balanceOfTrx(Resource):
    """Return balance of TRX."""
    
    @jwt_required
    def get(self, account_address):
        """Return balance of TRX."""

        logsOfError=''
        try:
            balance = tron.trx.get_balance(account_address, is_float=True)
            print(balance)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'balanceTrx':str(balance), 'logs':logsOfError}


@ns.route('/create_account')
class create_account(Resource):
    """Create blockchain account and return info about account."""
    
    def post(self):
        """Create blockchain account and return info about account."""

        logsOfError=''
        try:
            account = tron.create_account
            print(account)
        except Exception as e:
            logsOfError = logsOfError+str(e)
        return {'publicKey':str(account.public_key), 'base58':str(account.address.base58), 'hex':str( account.address.hex), 'privateKey':str(account.private_key), 'logs':logsOfError}


@ns.route('/oauth/authorize')
class authorize(Resource):
    """Authorization of users. If success return token to user."""

    @api.expect(oauth)
    def post(self):
        """Authorization of users. If success return token to user."""

        #connection = sqlite3.connect('rest_api/database/Users.db',check_same_thread=False)
        cursor = connection.cursor()
        print("234")
        # Input data
        data = request.get_json(force=True)
        login = data['login']
        password = data['password']

        cursor.execute("SELECT login, password, is_confirm FROM users WHERE login=(?)",(str(login),))
        print(cursor)
        arr_check = []
        for row in cursor:
            arr_check.append(row)
        print(arr_check)


        if len(arr_check)==0:
            return {"error":"wrong password or login"}, 401
        if arr_check[0][2]==0:
            return {"error": "you are email is not confirm"}, 401


        pw_hash=arr_check[0][1]
        cursor.close()
        if len(arr_check)==1 and bcrypt.check_password_hash(pw_hash, password):
            ret = {
                'access_token': create_access_token(identity=login),
                'refresh_token': create_refresh_token(identity=login),
                'expires_in':ACCESS_TOKEN_EXPIRES_IN,
                'token_type':'bearer'
            }

            return ret, 200
        else:
            return {"error":"wrong password or login"}, 401


@ns.route('/oauth/refresh')
class refreshToken(Resource):
    """Refresh token for simple authorization.""" 

    @jwt_refresh_token_required
    def post(self):
        """Refresh token for simple authorization."""

        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user),
            'refresh_token': create_refresh_token(identity=current_user),
            'expires_in':ACCESS_TOKEN_EXPIRES_IN,
            'token_type':'bearer'
        }
        return ret, 200




bcrypt = Bcrypt()
@ns.route('/oauth/registration')
class authorize(Resource):
    """Registration users. If success, insert into database and return data of blockchain account."""

    @api.expect(registration)
    def post(self):
        """Registration users. If success, insert into database and return data of blockchain account."""

        is_confirm=0
        cursor = connection.cursor()
        # Input data
        data = request.get_json(force=True)
        login = data['login']
        password = data['password']
        #public_key_hex = data['hex']

        cursor.execute("SELECT * FROM users WHERE login=(?)",(str(login),))
        #print(cursor)
        arr_check = []
        for row in cursor:
            arr_check.append(row)
        if len(arr_check)>0:
            return {"status":"Login is exist"}, 401
        else:
            created_account = createAccount_blockchain()
            public_key_hex = created_account['hex']
            pw_hash = bcrypt.generate_password_hash(password)
            sql = "INSERT INTO users (login, password, public_key_hex, is_confirm) VALUES ((?), (?), (?), (?));"
            val = (login, pw_hash, public_key_hex, is_confirm)
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
            send_confirmation_email(login)
            print(login, pw_hash, public_key_hex)
            getTokens_utils(public_key_hex)
            return created_account

mail = Mail()
def send_confirmation_email(user_email):
    """Send token on mail for confirm login."""

    confirm_serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt')
    
    
    msg = Message("Confirm email for platform chainMarket",
                body = 'Click for confirm email address: '+ API_EMAIL_CONFIRM_ADDRESS+token,
                sender="galym55010@gmail.com",
                recipients=[user_email])
    print("hello")
    mail.send(msg)
    return "sended"



@ns.route('/oauth/confirm_email/<token>')
class confirm_email(Resource):
    """Accept token for confirm login of users. If success, confirm login in database."""

    def get(self, token):
        """Accept token for confirm login of users. If success, confirm login in database."""

        logsOfError = ""
        try:
            confirm_serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
            print(email)
        except Exception as e:
            return {"status":"failed", "logs":str(e)},401
            
        try:
            cursor = connection.cursor()
            sql = "UPDATE users SET is_confirm=(?) where login=(?);"
            val=(1, email)
            cursor.execute(sql,val)
            connection.commit()
            cursor.close()
            status = "success"
        except Exception as e:
            status='failed'
            logsOfError+=str(e)
        return {"status": status, "logs":logsOfError},401
