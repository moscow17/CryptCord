import os
import hashlib

from base64 import b64encode, b64decode, urlsafe_b64decode, urlsafe_b64encode

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

from src.protocol.xchacha import *
from src.discord.requests import Communication

class RsaProtocol(object):

    def sign(self, pub, key, nonce):
        protocol = PKCS1_OAEP.new(pub)
        return b64encode(protocol.encrypt(f"{key} {urlsafe_b64encode(nonce).decode('utf-8')}".encode())).decode("utf-8")

    def unsign(self, content, priv):
        protocol = PKCS1_OAEP.new(priv)
        return protocol.decrypt(b64decode(content)).decode("utf-8")

class XChaChaProtocol(object):

    def encrypt(self, content, key, nonce):
        return b64encode(crypto_aead_xchacha20poly1305_ietf_encrypt(content.encode(), None, nonce, key.encode())).decode("utf-8")

    def decrypt(self, content, key, nonce):
        return crypto_aead_xchacha20poly1305_ietf_decrypt(b64decode(content), None, urlsafe_b64decode(nonce), key.encode()).decode()

class StandardProtocol(object):

    signer = RsaProtocol()
    cipher = XChaChaProtocol()

    comm = Communication()

    def __init__(self, client):
        self.client = client

    @property
    def key(self):
        return hashlib.sha256(os.urandom(24)).hexdigest()

    @property
    def private(self):
        return RSA.import_key(open("opt/mykeys/priv.pem").read())

    @property
    def public(self):
        return RSA.import_key(open(f"opt/keys/{self.client.uid}/pub.pem").read())

    def send(self, content):
        key = self.key[:32]
        nonce = generate_nonce()

        content = self.cipher.encrypt(content, key, nonce)
        key_msg = self.signer.sign(self.public, key, nonce)

        self.comm.send_message(self.client.uid, "key: " +  key_msg + "msg: " + content)

    def receive(self, content):
        message = content.split("msg: ")[1].split(" ")[0]
        key = content.split("key: ")[1].split("msg: ")[0]

        keystr = self.signer.unsign(key, self.private)

        key, nonce = keystr.split(" ")
        return self.cipher.decrypt(message, key, nonce)
