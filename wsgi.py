#!/usr/bin/env python
#coding=utf-8

#import falcon
import os
import json
from flask import Flask
from flask import request
from flask import Flask, make_response 

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply
from wechatpy.replies import create_reply
from wechatpy.replies import ArticlesReply


from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"
    
@application.route('/wechatconnect', methods=['GET', 'POST'])
def connect():
    if request.method == 'GET':
        args = request.args
        resp_body = ""
        for k, v in args.items():
            print(f"{k}: {v}")
        print(args)
        try:
            check_signature_str = check_signature(token='001001001001', signature=args['signature'], timestamp=args['timestamp'], nonce=args['nonce'])
            print(check_signature_str)
            resp_body = args["echostr"]
        except InvalidSignatureException:
            print("Error with check_signature")
            resp_body = "Error with check_signature"
            pass
        return resp_body
    elif request.method == 'POST':
        xml = request.stream.read()
        msg = parse_message(xml)
        print(msg)
        if msg.type == 'text':
            reply = TextReply(content=msg.content, message=msg)
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            ocr_text = '';
            try:
                cred = credential.Credential(
                os.environ.get("TENCENTCLOUD_SECRET_ID"),
                os.environ.get("TENCENTCLOUD_SECRET_KEY"))
                httpProfile = HttpProfile()
                httpProfile.endpoint = "ocr.tencentcloudapi.com"

                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                client = ocr_client.OcrClient(cred, "ap-hongkong", clientProfile)

                ocrreq = models.GeneralFastOCRRequest()
                ocrreq.ImageUrl = msg.image #发送过来的消息的url
                ocrres = client.GeneralFastOCR(ocrreq)
                print(ocrres.to_json_string())
                
                for x in   json.loads (  ocrres.to_json_string() ) ["TextDetections"]:
                    print(x["DetectedText"])
                    ocr_text.join.x["DetectedText"]

            except TencentCloudSDKException as err:
                    print(err)
            reply = ArticlesReply(message=msg)
            # simply use dict as article
            reply.add_article({
                'title': 'OCR Test',
                'description': ocr_text,
                'image': msg.image
                #'url': 'url'
            })        
        else:
            reply = TextReply(content='Hello,大哥，目前只支持文本和图片', message=msg)
        xml = reply.render()    
        print(reply)
        response = make_response(xml)
        response.content_type = 'application/xml'
        return response
        
if __name__ == "__main__":
    application.run()
    
