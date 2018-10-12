from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.functional import cached_property

from naclencryptedfields.backends.naclwrapper import NaClWrapper


class NaClEncryptedFieldMixin(object):
	"""
	NaClEncryptedFieldMixin will use PyNaCl to encrypt/decrypt data that is
	being put in/out of the database into application Django model fields. This
	package is largely based on the django-encrypted-fields package, which makes
	use of the outdated Keyczar library to encrypt fields.

	The only way to use this mixin is to set the NACL_FIELDS_KEY in settings.py
	to a base64 encoded key that matches the key size of the crypto_class used.
	The default crypto class - NaCl's SecretBox - takes a 32	byte key.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initialize the NaClEncryptedFieldMixin with the optional setting:
		* crypto_class: A custom class that is extended from CryptoWrapper.
		"""
		crypto_class = kwargs.pop('crypto_class', NaClWrapper)

		key = settings.NACL_FIELDS_KEY
		if not key:
			raise ImproperlyConfigured(
				'You must set settings.NACL_FIELDS_KEY to use this library.'
			)

		self._crypto_box = crypto_class(key)

		super().__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'TextField'

	@cached_property
	def validators(self):
		# Temporarily pretend to be whatever type of field we're mixed in with to
		# pass validation (needed for IntegerField and subclasses).
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


class NaClEncryptedBooleanField(NaClEncryptedFieldMixin, models.BooleanField):
	pass


class NaClEncryptedCharField(NaClEncryptedFieldMixin, models.CharField):
	pass


class NaClEncryptedDateTimeField(NaClEncryptedFieldMixin, models.DateTimeField):
	pass


class NaClEncryptedDateField(NaClEncryptedFieldMixin, models.DateField):
	pass


class NaClEncryptedEmailField(NaClEncryptedFieldMixin, models.EmailField):
	pass


class NaClEncryptedFloatField(NaClEncryptedFieldMixin, models.FloatField):
	pass


class NaClEncryptedIntegerField(NaClEncryptedFieldMixin, models.IntegerField):
	pass


class NaClEncryptedTextField(NaClEncryptedFieldMixin, models.TextField):
	pass
