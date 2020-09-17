# from pyDes import des, PAD_PKCS5, ECB
# from rsa import common, transform, core
import sys
sys.path.append(r'./')
from myutils import *
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import base64,os,rsa,hashlib,json,requests,threading

# from myutils import des, PAD_PKCS5, ECB,common, transform, core


serverRSAPublicKey=""
clientRSAPublicKey=""
clientRSAPrivateKey=""
url=""


@dispatcher.add_method
def RetrieveFile(filename,_url):
    global url
    url=_url
    print("serverUrl:%s\nfilename:%s\n"%(url,filename))
    th=threading.Thread(target=downloadFile,args=(filename,))
    th.start()
    return {"status":"success"}


    
@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')
    

def downloadFile(filename):
    global serverRSAPublicKey,serverRSAPrivateKey,clientRSAPublicKey,url

    (clientRSAPublicKey,clientRSAPrivateKey)=rsa.newkeys(512)
    print("client 公钥:\n%s\n私钥:\n:%s" % (clientRSAPublicKey, clientRSAPrivateKey))

    params={"clientRSAPublicKey":b64enc(clientRSAPublicKey.save_pkcs1())}
    res=RPCCall(url,"ExchangePublicKey",params)
    serverRSAPublicKey=rsa.PublicKey.load_pkcs1(b64dec(res["serverRSAPublicKey"]))

    res=RPCCall(url,"GetFile",{"filename":filename})

    DESKey=rsaDecrypt(b64dec(res["encDESKey"]),clientRSAPrivateKey)
    md5Str=rsaDecrypt2(b64dec(res["encMD5"]),serverRSAPublicKey).decode('utf-8')
    desObj = des(DESKey, ECB, DESKey, padmode=PAD_PKCS5)
    encFile=b64dec(res["encFile"])
    content=desObj.decrypt(encFile)
    print("get file: %s."%content)
    if getMD5(content)!=md5Str:
        print("Different md5 code.")
        exit(1)
    else:
        print("Correct md5 code.")
    
    f=open("out.txt","wb")
    f.write(content)
    f.close()
    print("download done.")



def client():
    global serverRSAPublicKey,serverRSAPrivateKey,clientRSAPublicKey,url
    (clientRSAPublicKey,clientRSAPrivateKey)=rsa.newkeys(512)
    print("client 公钥:\n%s\n私钥:\n:%s" % (clientRSAPublicKey, clientRSAPrivateKey))
    run_simple('localhost', 4001, application)

def main():
    print("client")
    #主动取文件不用开server，但被动取文件需要server
    #主动取即downloadfile
    #被动取则client


    
    #------------------------------------------------------

    # func="ExchangePublicKey"
    # params={"clientRSAPublicKey":b64enc(clientRSAPublicKey.save_pkcs1())}
    # res=RPCCall(url,func,params)
    # serverRSAPublicKey=rsa.PublicKey.load_pkcs1(b64dec(res["serverRSAPublicKey"]))

    # res=RPCCall(url,"GetFile",{"filename":"test.txt"})

    # DESKey=rsaDecrypt(b64dec(res["encDESKey"]),clientRSAPrivateKey)
    # md5Str=rsaDecrypt2(b64dec(res["encMD5"]),serverRSAPublicKey).decode('utf-8')
    # desObj = des(DESKey, ECB, DESKey, padmode=PAD_PKCS5)
    # encFile=b64dec(res["encFile"])
    # content=desObj.decrypt(encFile)
    # print("get file: %s."%content)
    # if getMD5(content)!=md5Str:
    #     print("Different md5 code.")
    #     exit(1)
    # else:
    #     print("Correct md5 code.")
    
    # f=open("out.txt","wb")
    # f.write(content)
    # f.close()
    # print("download done.")

    #----------------------------------------------------


    # url = "http://localhost:4000/jsonrpc"

    # bin='hello base64'.encode('utf-8')#b'\xff\xe4'
    # b64=base64.b64encode(bin)
    # b64=bytes.decode(b64)
    # print("b64str: "+b64)
    

    # # Example echo method
    # payload = {
    #     "method": "foobar",
    #     "params": {"bin":b64,"foo":"haha","bar":"666"},#["echome!"],
    #     "jsonrpc": "2.0",
    #     "id": 0,
    # }
    # response = requests.post(url, json=payload).json()
    # print(response["result"])
    # print("------")
    # # assert response["result"] == "echome!"
    # assert response["jsonrpc"]
    # assert response["id"] == 0

if __name__ == "__main__":
    main()



