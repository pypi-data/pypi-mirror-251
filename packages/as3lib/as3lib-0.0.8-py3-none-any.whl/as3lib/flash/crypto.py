from as3lib import toplevel as as3
from os import urandom
from binascii import b2a_hex

def generateRandomBytes(numberRandomBytes:Union[int,as3.uint,as3.Int]):
   #!return flash bytearray instead of string
   try:
      return f"{b2a_hex(urandom(int(numberRandomBytes)))}"[2:][:(int(numberRandomBytes)*2)]
   except:
      as3.Error("generateRandomBytes; Could not generate random bytes")