
from .cryptowrapper import CryptoWrapper

import base64

import nacl.pwhash
import nacl.secret
import nacl.utils


# Simple wrapper around PyNaCl to standardize the initialization of the crypter
# object and allow for others to extend as needed.
class NaClWrapperException(Exception):
	pass


class NaClWrapper(CryptoWrapper):
	def __init__(self, keydata, *args, **kwargs):
		self.crypter = nacl.secret.SecretBox(keydata)

	def encrypt(self, plaintext):
		ciphertext = self.crypter.encrypt(plaintext.encode())
		return base64.b64encode(ciphertext).decode()

	def decrypt(self, ciphertext):
		ciphertext = base64.b64decode(ciphertext.encode())
		return self.crypter.decrypt(ciphertext).decode()

	@staticmethod
	def createKey():
		return nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
