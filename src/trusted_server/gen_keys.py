from processing import ABE, SelfAES
from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup
from Crypto.PublicKey import ECC
import os


aes_key = os.urandom(32)
with open("./keys/aes.key", "wb") as f:
    f.write(aes_key)

pairing_group = PairingGroup("SS512")
abe = ABE()
pk, mk = abe.setupKey()

aes = SelfAES()
with open('./keys/pk_key', 'wb') as f:
    f.write(aes.encrypt(objectToBytes(pk, pairing_group)))
with open('./keys/mk_key', 'wb') as f:
    f.write(aes.encrypt(objectToBytes(mk, pairing_group)))
    
private_key = ECC.generate(curve='ed25519')
public_key = private_key.public_key()

private_key_pem = private_key.export_key(format='PEM')
public_key_pem = public_key.export_key(format='PEM')

with open('./keys/jwtkey_priv.pem.enc', 'wb') as f:
    f.write(aes.encrypt(private_key_pem))
with open('./keys/jwtkey_pub.pem', 'wb') as f:
    f.write(public_key_pem.encode())