from pyDes import des, PAD_PKCS5, ECB
from rsa import common, transform, core
import base64,os,rsa,hashlib,requests

def _pad_for_encryption(message, target_length):
 
    max_msglength = target_length - 11
    msglength = len(message)
 
    if msglength > max_msglength:
        raise OverflowError(
            "%i bytes needed for message, but there is only"
            " space for %i" % (msglength, max_msglength)
        )
 
    padding = b""
    padding_length = target_length - msglength - 3
 
    while len(padding) < padding_length:
        needed_bytes = padding_length - len(padding)
        new_padding = os.urandom(needed_bytes + 5)
        new_padding = new_padding.replace(b"\x00", b"")
        padding = padding + new_padding[:needed_bytes]
 
    assert len(padding) == padding_length
 
    return b"".join([b"\x00\x02", padding, b"\x00", message])
 
def decrypt(data: bytes, d, n):
    num = transform.bytes2int(data)
    decrypto = core.decrypt_int(num, d, n)
    out = transform.int2bytes(decrypto)
    sep_idx = out.index(b"\x00", 2)
    out = out[sep_idx + 1 :]
    return out
 
def encrypt(data: bytes, d, n):
    keylength = common.byte_size(n)
    padded = _pad_for_encryption(data, keylength)
    num = transform.bytes2int(padded)
    decrypto = core.encrypt_int(num, d, n)
    out = transform.int2bytes(decrypto)
    return out

def rsaEncrypt2(content, key):
    return encrypt(content, key.d,key.n)
def rsaDecrypt2(content, key):
    return decrypt(content, key.e,key.n)


#bytes to str
def b64enc(content):
    return bytes.decode(base64.b64encode(content))

#str to bytes
def b64dec(str):
    return base64.b64decode(str.encode())

def rsaEncrypt(content, key):
    # content是bytes[]
    crypto = rsa.encrypt(content, key)
    return crypto

def rsaDecrypt(content, key):
    # content是bytes[]
    ret = rsa.decrypt(content, key)
    return ret


def getMD5(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()


def RPCCall(url,func,params):
    # url = "http://localhost:4000/jsonrpc"

    payload = {
        "method": func,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, json=payload).json()
    assert response["jsonrpc"]
    assert response["id"] == 0
    print(response["result"])
    print("------")
    return response["result"]