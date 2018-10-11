
from naclencryptedfields.backends.cryptowrapper import CryptoWrapper

import base64


# Test class that uses XOR to encrypt. Requirements are to implement encrypt()
# and decrypt(). NOTE: do not use this in production.
class TestCryptoWrapper(CryptoWrapper):
	def __init__(self, keydata, *args, **kwargs):
		self.key = keydata

	def encrypt(self, plaintext):
		enc = b''.join(chr(ord(itr) ^ self.key[idx % len(self.key)]).encode()
		               for idx, itr in enumerate(plaintext))
		return base64.b64encode(enc).decode()

	def decrypt(self, ciphertext):
		enc = base64.b64decode(ciphertext.encode()).decode()
		return ''.join(chr(ord(itr) ^ self.key[idx % len(self.key)])
		               for idx, itr in enumerate(enc))
