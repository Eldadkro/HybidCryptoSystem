from binascii import hexlify
from ellipticcurve import signature
import ellipticcurve
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve import publicKey
from Knapsack.Knapsak import Knapsack
from pyDes.pyDes import PAD_PKCS5, des, triple_des
import ellipticcurve.ecdsa as ec
from ellipticcurve.signature import Signature
import random
import Knapsack as ks
import pyDes as ds
import json


class player():

    def __init__(self, name: str, knap_self: Knapsack, knap_other: Knapsack, ecdsa_self: ec.ElipticDSA,
                 ecdsa_other: ec.ElipticDSA):
        self.des = None
        self.knap_self = knap_self
        self.knap_other = knap_other
        self.ecdsa_self = ecdsa_self
        self.ecdsa_other = ecdsa_other
        self.name = name

    def keyexchange(self, msg=None):
        if(msg == None):
            _3deskey = self._gen3DesKey()
            self.des = triple_des(_3deskey,padmode=PAD_PKCS5)
            sign = self.ecdsa_self.sign(_3deskey)
            return self.knap_other.cipher(json.dumps({
                "key" : _3deskey,
                "sign" : [sign.r,sign.s]
            }))
        if(msg != None):
            msg = self.knap_self.decipher(msg)
            msg = json.loads(msg)
            sign = Signature(msg["sign"][0],msg["sign"][1])
            if(self.ecdsa_other.verify(msg['key'],sign) == True):
                self.des = triple_des(msg["key"],padmode=PAD_PKCS5)
                return True
        return False

    # TODO
    def send(self, msg, name):
        sign = self.ecdsa_self.sign(msg)
        return self.des.encrypt(json.dumps({
            "src": self.name,
            "dest": name,
            "msg": msg,
            "sign": [sign.r, sign.s]
        }))

    # TODO

    def recive(self, y):
        x = self.des.decrypt(y)
        msg = json.loads(x)
        m = msg["msg"]
        sign = Signature(msg["sign"][0], msg["sign"][1])
        return (msg, self.ecdsa_other.verify(m, sign))

    # TODO

    @classmethod
    def _gen3DesKey(cls):
        hex_digits = set('0123456789ABCDEF')
        result = ""
        for digit in range(24):
            cur_digit = random.sample(hex_digits, 1)[0]
            result += cur_digit
        return result

    def __repr__(self) -> str:
        return self.name
