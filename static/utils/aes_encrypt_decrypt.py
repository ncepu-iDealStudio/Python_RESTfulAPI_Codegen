import base64
from Crypto.Cipher import AES
from utils.loggings import loggings


class AESEncryptDecrypt:
    key = None  # 将密钥转换为字符型数据
    mode = AES.MODE_ECB  # 操作模式选择ECB

    @classmethod
    def encrypt(cls, text=None):
        """加密函数"""
        if cls.key:
            pass
        else:
            from flask_sqlalchemy import current_app
            cls.key = current_app.config.get('SECRET_KEY').encode()

        file_aes = AES.new(cls.key, cls.mode)  # 创建AES加密对象
        # while len(text) % 16 != 0:  # 对字节型数据进行长度判断
        #     text += '\0'  # 如果字节型数据长度不是16倍整数就进行补充
        # text = text.encode('utf-8')  # 明文必须编码成字节流数据，即数据类型为bytes
        text = text.encode('utf-8')  # 明文必须编码成字节流数据，即数据类型为bytes
        while len(text) % 16 != 0:  # 对字节型数据进行长度判断
            text += '\0'.encode('utf-8')  # 如果字节型数据长度不是16倍整数就进行补充
        en_text = file_aes.encrypt(text)  # 明文进行加密，返回加密后的字节流数据
        return str(base64.b64encode(en_text), encoding='utf-8')  # 将加密后得到的字节流数据进行base64编码并再转换为unicode类型

    @classmethod
    def decrypt(cls, text):
        """解密函数"""
        if cls.key:
            pass
        else:
            from flask_sqlalchemy import current_app
            cls.key = current_app.config.get('SECRET_KEY').encode()
        try:
            file_aes = AES.new(cls.key, cls.mode)
            text = bytes(text, encoding='utf-8')  # 将密文转换为bytes，此时的密文还是由basen64编码过的
            text = base64.b64decode(text)  # 对密文再进行base64解码
            de_text = file_aes.decrypt(text)  # 密文进行解密，返回明文的bytes
            return str(de_text, encoding='utf-8').replace('\0', '')  # 将解密后得到的bytes型数据转换为str型，并去除末尾的填充

        except Exception as e:
            loggings.exception(1, e)
            return None
