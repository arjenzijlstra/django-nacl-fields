import base64
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from naclencryptedfields.backends.naclwrapper import NaClWrapper


class NaClEncryptedFieldException(Exception):
	pass


class NaClEncryptedFieldMixin(object):
	"""
	NaClEncryptedFieldMixin will use PyNaCl to encrypt/decrypt data that is
	being put in/out of the database into application Django model fields. This
	package is largely based on the django-encrypted-fields package, which makes
	use of the outdated Keyczar library to encrypt fields, but

	There are three options to use this mixin.

	- If no key is set, the Django SECRET_KEY is used to encrypt the fields.
	- The recommended way is to set a custom key, set the NACL_FIELDS_KEY in
	  settings.py to a base64 encoded key that matches the key size of the
	  crypto_class used. The default crypto class - NaCl's SecretBox - takes a
	  32 byte key.
	- It is also possible to set a specific encryption key per field. Such as:
	  data = NaclEncryptedCharField(..., key='c3VwZXJfc2VjcmV0X2tleQ==')
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the NaClEncryptedFieldMixin with the following optional settings:
		* key: The key to encrypt this field with.
		* crypto_class: A custom class that is extended from CryptoWrapper.
		"""
		crypto_class = kwargs.pop('crypto_class', NaClWrapper)

		key = kwargs.pop('key', None)  # does this field have a specific key?
		if not key:
			# if no key is set, just use the Django SECRET_KEY
			key = getattr(settings, 'NACL_FIELDS_KEY', settings.SECRET_KEY)
			key = base64.b64decode(key)

		self._crypto_box = crypto_class(key)

		super().__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'TextField'

	# https://github.com/orcasgit/django-fernet-fields/blob/master/fernet_fields/fields.py
	@cached_property
	def validators(self):
		# Temporarily pretend to be whatever type of field we're masquerading
		# as, for purposes of constructing validators (needed for
		# IntegerField and subclasses).
		self.__dict__['_internal_type'] = super().get_internal_type()
		try:
			return super().validators
		finally:
			del self.__dict__['_internal_type']

	def from_db_value(self, value, expression, connection, context):
		if value is None or value == '' or not isinstance(value, str):
			return value

		value = self._crypto_box.decrypt(value)
		return super().to_python(value)

	def get_db_prep_value(self, value, connection, prepared=False):
		if value is None or value == '':
			return value

		if not isinstance(value, str):
			value = str(value)

		return self._crypto_box.encrypt(value)


class NaClEncryptedCharField(NaClEncryptedFieldMixin, models.CharField):
	pass


class NaClEncryptedTextField(NaClEncryptedFieldMixin, models.TextField):
	pass


class NaClEncryptedDateTimeField(NaClEncryptedFieldMixin, models.DateTimeField):
	pass


class NaClEncryptedIntegerField(NaClEncryptedFieldMixin, models.IntegerField):
	pass


class NaClEncryptedDateField(NaClEncryptedFieldMixin, models.DateField):
	pass


class NaClEncryptedFloatField(NaClEncryptedFieldMixin, models.FloatField):
	pass


class NaClEncryptedEmailField(NaClEncryptedFieldMixin, models.EmailField):
	pass


class NaClEncryptedBooleanField(NaClEncryptedFieldMixin, models.BooleanField):
	pass
