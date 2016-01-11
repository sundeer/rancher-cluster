from Crypto.PublicKey import RSA
from invoke import ctask as task
import json

def generate_OpenSSH(ctx, bits=2048):
    '''
    Generate an RSA OpenSSH keypair with an exponent of 65537
    param: bits The key length in bits
    Return private key and public key
    '''
    private_key = RSA.generate(bits, e=65537)
    public_key = private_key.publickey()
    str_private_key = private_key.exportKey("PEM")
    str_public_key = public_key.exportKey("OpenSSH")
    return str_private_key, str_public_key


def print_json(json_like_object):
    print(json.dumps(json_like_object, sort_keys=True, indent=4, separators=(',', ': ')))
