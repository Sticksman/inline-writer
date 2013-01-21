from Crypto.Cipher import AES
import base64
import os
from django.conf import settings
import time

def encrypt_string(string):
    string = str(string)
    # the block size for the cipher object; must be 16, 24, or 32 for AES
    BLOCK_SIZE = 16

    # the character used for padding--with a block cipher such as AES, the value
    # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
    # used to ensure that your value is always a multiple of BLOCK_SIZE
    PADDING = '{'

    # one-liner to sufficiently pad the text to be encrypted
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    # generate a secret key (must be 16 chars)
    secret = settings.APP_SECRET  

    # create a cipher object using the random secret
    cipher = AES.new(secret)

    # encode a string
    encoded = EncodeAES(cipher, string)
    encoded = encoded.replace("/", "-")
    encoded = encoded.replace("+", "_")
    return encoded


def decrypt_string(string):
    string = string.replace("-","/")
    string = string.replace("_","+")

    # the block size for the cipher object; must be 16, 24, or 32 for AES
    BLOCK_SIZE = 16

    # the character used for padding--with a block cipher such as AES, the value
    # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
    # used to ensure that your value is always a multiple of BLOCK_SIZE
    PADDING = '{'

    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

    # generate a secret key (must be 16 chars)
    secret = settings.APP_SECRET  

    # create a cipher object using the random secret
    cipher = AES.new(secret)


    # decode the encoded string
    decoded = DecodeAES(cipher, string)

    return decoded

OwnerPermission = "com.CircleUp.permission:Owner"

def encode_user_id(unencoded_id, permission=None):
    #TODO Encode the id
    unencoded = str(unencoded_id)
    if permission:
        unencoded = "%s+%s+%s" % (unencoded, permission, time.time())
    encoded = encrypt_string(unencoded)
    return encoded

def validate_user_id(token, permission):
    uid, perm = decode_user_id_with_permission(token)
    if perm == permission:
        return uid
    return None

def decode_user_id(token):
    return decode_user_id_with_permission(token)[0]

def decode_user_id_with_permission(token):
    decoded = decrypt_string(token)
    parts = decoded.split('+')    
    if len(parts) == 3:
        return parts[0], parts[1]
    elif len(parts) == 1:
        return parts[0], None
    raise ValueError, "The token %s has the wrong format" % token
