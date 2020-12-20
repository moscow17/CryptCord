import os
from Cryptodome.PublicKey import RSA

async def save_key(message, key):
    path = "opt/keys/%s" %(message.channel.id)

    print(path)
    with open(path + "/pub.pem", "w") as fp:
        content = await key.read()
        fp.write(content.decode())

def make_key():
    if not os.path.isdir("opt/mykeys"):

        key = RSA.generate(4096)

        os.mkdir("opt/mykeys")
        with open('opt/mykeys/pub.pem','wb') as fp:
            fp.write(key.publickey().export_key())
        with open('opt/mykeys/priv.pem','wb') as fp:
            fp.write(key.export_key('PEM'))
