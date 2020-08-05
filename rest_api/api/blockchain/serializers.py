#!flask/bin/python
"""
Blockchain API
Api for connecting blockchain technology with a mobile application.
Blockchain: TRON;

Copyright (c) 2020 IDET.kz
Written by Galymzhan Abdymanap.
Version 1.0
"""

from flask_restplus import fields
from rest_api.api.restplus import api


getChecks = api.model('getChecks', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    
})
getWallet = api.model('getWallet', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    
})
balanceOfToken = api.model('balanceOfToken', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    
})
balanceOfTrx = api.model('balanceOfTrx', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    
})
purchaseGoods = api.model('purchaseGoods', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchain'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='ID of goods on Blockchain Market'),
    'amounts_goods':fields.List(fields.Integer,readOnly=True, description='Amount of goods for purchase on Blockchain Market'),
})
confirmGoods = api.model('confirmGoods', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchain'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='ID of goods on Blockchain Market'),
    'id_check':fields.Integer(readOnly=True, description='ID of check to confirm purchase on Blockchain Market') 
})
saleOfGoods = api.model('saleOfGoods', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchain'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='ID of goods on Blockchain Market'),
    'amounts_goods':fields.List(fields.Integer,readOnly=True, description='Amount of goods for purchase on Blockchain Market'),
})
cancelOfPurchase = api.model('cancelOfPurchase', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchainy'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='ID of goods on Blockchain Market'),
    'id_check':fields.Integer(readOnly=True, description='ID of check to cancel purchase on Blockchain Market') 
})
freeze_balance = api.model('freeze_balance', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchain'),
    'amount':fields.Integer(readOnly=True, description='Amount of TRX for freeze'),
    'resource':fields.String(readOnly=True, description='ENERGY or BANDWIDTH'),

})
unfreeze_balance = api.model('unfreeze_balance', {
    'account_address': fields.String(readOnly=True, description='Account address on Blockchain'),
    'privateKey':fields.String(readOnly=True, description='Private key of account on Blockchain'),
    'resource':fields.String(readOnly=True, description='ENERGY or BANDWIDTH'),

})
registration = api.model('registration', {
    'login': fields.String(readOnly=True, description='Login for mobile app'),
    'password':fields.String(readOnly=True, description='Password for mobile app'),
      
})
oauth = api.model('oauth', {
    'login': fields.String(readOnly=True, description='Login for mobile app'),
    'password':fields.String(readOnly=True, description='Password for mobile app'),
    
})


