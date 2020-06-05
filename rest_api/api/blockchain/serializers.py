from flask_restplus import fields
from rest_api.api.restplus import api


getChecks = api.model('getChecks', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    
})
getWallet = api.model('getWallet', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    
})
balanceOfToken = api.model('balanceOfToken', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    
})
balanceOfTrx = api.model('balanceOfTrx', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    
})
purchaseGoods = api.model('purchaseGoods', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'amounts_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'timestamp':fields.String(readOnly=True, description='The unique identifier of a blog category'),
})
confirmGoods = api.model('confirmGoods', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'id_check':fields.Integer(readOnly=True, description='The unique identifier of a blog category') 
})
saleOfGoods = api.model('saleOfGoods', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'amounts_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'timestamp':fields.String(readOnly=True, description='The unique identifier of a blog category'),
})
cancelOfPurchase = api.model('cancelOfPurchase', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'id_goods':fields.List(fields.Integer,readOnly=True, description='The unique identifier of a blog category'),
    'id_check':fields.Integer(readOnly=True, description='The unique identifier of a blog category') 
})
freeze_balance = api.model('freeze_balance', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'amount':fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'resource':fields.String(readOnly=True, description='The unique identifier of a blog category'),

})
unfreeze_balance = api.model('unfreeze_balance', {
    'account_address': fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'privateKey':fields.String(readOnly=True, description='The unique identifier of a blog category'),
    'resource':fields.String(readOnly=True, description='The unique identifier of a blog category'),

})



