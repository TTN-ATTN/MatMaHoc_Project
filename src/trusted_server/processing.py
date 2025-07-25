from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.core.engine.util import objectToBytes, bytesToObject
from Crypto.Cipher import AES
from hashlib import sha512
import jwt
import time
import subprocess
    
class SelfAES:
    def __init__(self):
        self.key = open("./keys/aes.key", "rb").read()

    def encrypt(self, data):
        if type(data) != type(b''):
            data = data.encode()
        
        Cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = Cipher.encrypt_and_digest(data)
        
        return Cipher.nonce + ciphertext + tag
    
    def decrypt(self, data):
        Cipher = AES.new(self.key, AES.MODE_GCM, data[:16])
        
        return Cipher.decrypt_and_verify(data[16:-16], data[-16:])
        
class ABE:
    def __init__(self):
        self.group = PairingGroup('SS512')
        self.cpabe = CPabe_BSW07(self.group)
    
    def setupKey(self):
        return self.cpabe.setup()
    
    def getMasterPublicKey(self):
        aes = SelfAES()
        with open('./keys/pk_key', 'rb') as f:
            pk = aes.decrypt(f.read())
            
            return pk
    
    def genDecryptKey(self, attribute: list):
        aes = SelfAES()
        with open('./keys/pk_key', 'rb') as f:
            tmp = aes.decrypt(f.read())
            self.pk = bytesToObject(tmp, self.group)
        with open('./keys/mk_key', 'rb') as f:
            tmp = aes.decrypt(f.read())
            self.mk = bytesToObject(tmp, self.group)

        dk = self.cpabe.keygen(self.pk, self.mk, attribute)
        
        return objectToBytes(dk, self.group)
    
class SelfJWT:
    def __init__(self):
        with open("./keys/jwtkey_priv.pem.enc", "rb") as f:
            encrypted_key = f.read()
            aes = SelfAES()
            self.key = aes.decrypt(encrypted_key)
    
    def encode(self, attribute, user_id):
        exp_time = str(round(time.time()) + 3600) 

        data = {
            'user_id': user_id,
            'attribute':attribute,
            'expiry':exp_time
        }

        enc_data = jwt.encode(
            data, self.key, algorithm='EdDSA'
        )
        
        return enc_data
    
class Hash:
    def hashing(data):
        if type(data) != type(b''):
            data = data.encode()
        
        return sha512(data).hexdigest()