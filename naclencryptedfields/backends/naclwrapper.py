
from .cryptowrapper import CryptoWrapper

import base64

import nacl.pwhash
import nacl.utils
import nacl.secret


# Simple wrapper around PyNaCl to standardise the initialization of the box
# object and allow for others to extend as needed.
class NaClWrapper(CryptoWrapper):
	salt = 'tHeQ/aaj8e4Z9Jj33+xZOQ=='

	def __init__(self, keydata, apply_kdf=False, *args, **kwargs):
		key = base64.b64decode(keydata)
		if apply_kdf or len(keydata) != nacl.secret.SecretBox.KEY_SIZE:
			key = NaClWrapper.kdf(key)

		self.box = nacl.secret.SecretBox(key)

	def encrypt(self, plaintext):
		ciphertext = self.box.encrypt(plaintext.encode())
		return base64.b64encode(ciphertext).decode()

	def decrypt(self, ciphertext):
		ciphertext = base64.b64decode(ciphertext.encode())
		return self.box.decrypt(ciphertext).decode()

	@staticmethod
	def createKey():
		return base64.b64encode(nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE))

	@staticmethod
	def kdf(password):
		return nacl.pwhash.argon2i.kdf(nacl.secret.SecretBox.KEY_SIZE,
		                               password.encode(),
		                               base64.b64decode(NaClWrapper.salt),
		                               opslimit=nacl.pwhash.argon2i.OPSLIMIT_MIN,
		                               memlimit=nacl.pwhash.argon2i.MEMLIMIT_MIN)
