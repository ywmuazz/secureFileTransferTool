# coding=UTF-8

# 监听

# 请求到来

import sys
# sys.path.append(r'./')
from myutils import *

from http.server import BaseHTTPRequestHandler, HTTPServer
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from client import downloadFile
import base64,os,hashlib,rsa,threading


#
serverRSAPublicKey = ""
serverRSAPrivateKey = ""
clientRSAPublicKey = ""
serverUrl="http://localhost:4000/jsonrpc"
toSendFilename=""
#

@dispatcher.add_method
def RetrieveFile(filename,url):
    print("serverUrl:%s\nfilename:%s\n"%(url,filename))
    th=threading.Thread(target=downloadFile,args=(filename,url,))
    th.start()
    return {"status":"success"}

@dispatcher.add_method
def foobar(**kwargs):
    print(kwargs["bin"])
    b64 = kwargs["bin"]
    print(base64.b64decode(b64).decode("utf-8"))
    return kwargs["foo"] + kwargs["bar"]


@dispatcher.add_method
def ExchangePublicKey(**kwargs):
    global clientRSAPublicKey, serverRSAPublicKey
    clientRSAPublicKey = rsa.PublicKey.load_pkcs1(
        b64dec(kwargs["clientRSAPublicKey"]))
    print(clientRSAPublicKey)
    return {"serverRSAPublicKey": b64enc(serverRSAPublicKey.save_pkcs1())}


@dispatcher.add_method
def GetFile(**kwargs):
    filename = kwargs["filename"]
    # 生成des密钥
    DESKey = os.urandom(8)
    print("DES key: %s" % DESKey)

    # 读取文件
    file = open(filename, "rb")
    content = file.read()

    # 若不为utf-8会报错
    print("file: "+content.decode('utf-8'))
    file.close()

    # 对文件做md5
    md5Str = getMD5(content)
    print("md5Str: "+md5Str)

    # rsa加密
    encDESKey = rsaEncrypt(DESKey, clientRSAPublicKey)
    encMD5 = rsaEncrypt2(md5Str.encode('utf-8'), serverRSAPrivateKey)

    # des加密文件
    desObj = des(DESKey, ECB, DESKey, padmode=PAD_PKCS5)
    encFile = desObj.encrypt(content)

    # 拼成json之前先转成base64
    return {
        "encDESKey": b64enc(encDESKey),
        "encFile": b64enc(encFile),
        "encMD5": b64enc(encMD5),
    }

    # 读文件
    # md5
    # rsa加密deskey,md5
    # des加密文件
    # 拼成json





@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


def sendFile(filename,targetUrl):
    global toSendFilename
    toSendFilename=filename
    res=RPCCall(targetUrl,"RetrieveFile",{"filename":filename,"url":serverUrl})
    if res["status"]!="success":
        print("Send File failed.")

#只要是发文件就要开server,被动发不用send，主动发需要sendFile

#server是非阻塞的
def server(port):
    global serverUrl
    serverUrl="http://localhost:%d/jsonrpc"%port
    # 生成server rsa public private key
    global serverRSAPublicKey,serverRSAPrivateKey
    (serverRSAPublicKey, serverRSAPrivateKey) = rsa.newkeys(512)
    print("server 公钥:\n%s\n私钥:\n:%s" %
          (serverRSAPublicKey, serverRSAPrivateKey))

    th=threading.Thread(target=run_simple,args=('localhost', port, application))
    th.start()

    #sendFile("test.txt","http://localhost:4001/jsonrpc")



if __name__ == '__main__':
    print()
    # server()
    # run_simple('localhost', 4000, application)


# class RequestHandler(BaseHTTPRequestHandler):
#     Page = '''\
#         <html>
#         <body>
#         <p>Hello,web!</p>
#         </body>
#         </html>
#     '''

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-Type", "text/html")
#         self.send_header("Content-Length", str(len(self.Page)))
#         self.end_headers()
#         self.wfile.write(self.Page.encode('utf-8'))


# if __name__=='__main__':
    # print("hahaha. ")
    # serverAddress=('',8080)
    # server=HTTPServer(serverAddress,RequestHandler)
    # server.serve_forever()


# def jianting():
    # 记录b发来的公钥
    # 生成rsa公私钥
    # 发送给b
    # 生成des秘钥
    # 用b公 加密 des秘钥
    # 读取文件用des加密
    # 对文件做md5用a的私钥加密
    # 三个打包
    # 发
