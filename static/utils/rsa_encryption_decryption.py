from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from flask import current_app


class RSAEncryptionDecryption():
    """
    用于解密前端的密码
    """
    def __init__(self):
        self.public_key = current_app.config["PUBLIC_KEY"]
        self.private_key = current_app.config["PRIVATE_KEY"]

    # RSA加密
    def encrypt(self, message):

        # 数据类型也可以这样转换成byte
        # bytes(message, "utf-8")

        # 导入配置文件的公钥
        public_key = RSA.importKey(self.public_key)

        # 生成对象
        cipher = Cipher_pkcs1_v1_5.new(public_key)

        # 通过生成的对象加密message明文，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
        cipher_text = base64.b64encode(cipher.encrypt(message.encode("utf-8")))

        return cipher_text

    # RSA 解密
    def decrypt(self, cipher_text):
        # 导入读取到的私钥
        private_key = RSA.importKey(self.private_key)

        # 生成对象
        cipher = Cipher_pkcs1_v1_5.new(private_key)

        try:
            # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
            text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR").decode("utf-8")
        except Exception as e:
            current_app.logger.error(e)
            return None
        return text


