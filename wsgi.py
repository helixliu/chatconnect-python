#!/usr/bin/env python
#coding=utf-8

#import falcon
from flask import Flask
from flask import request

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply


application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"
    
@application.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'GET':
        args = request.args
        print(args)
        try:
            check_signature(token='001001001001', signature=args['signature'], timestamp=args['timestamp'], nonce=args['nonce'])
            resp_body = (args['echostr'])
        except InvalidSignatureException:
            pass
        return resp_body
    return 'You are not logged in'

if __name__ == "__main__":
    application.run()
    
"""    
class Connect(object):
#接受微信服务器注册
    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='001001001001', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200
#处理微信消息
    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            reply = TextReply(content=msg.content, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)
"""


