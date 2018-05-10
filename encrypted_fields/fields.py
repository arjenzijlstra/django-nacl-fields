
import django
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property

from .backends.naclwrapper import NaClWrapper


class EncryptedFieldException(Exception):
	pass


class EncryptedFieldMixin(object):
	"""
	EncryptedFieldMixin will use NaCl to encrypt/decrypt data that is being
	marshalled in/out of the database into application Django model fields.

	This is very helpful in ensuring that data at rest is encrypted and
	minimizing the effects of SQL Injection or insider access to sensitive
	databases containing sensitive information.

	The most basic use of this mixin is to have a single encryption key for all
	data in your database. This lives in a Keyczar key directory specified by:
	the setting - settings.ENCRYPTED_FIELDS_KEYDIR -

	Optionally, you can name specific encryption keys for data-specific
	purposes in your model such as:
		special_data = EncrytpedCharField( ..., key='special_data' )

	The Mixin will handle the encryption/decryption seamlessly, but native
	SQL queries may need a way to filter data that is encrypted. Using the
	optional 'prefix' kwarg will prepend a static identifier to your encrypted
	data before it is written to the database.

	Encrypting data will significantly change the size of the data being stored
	and this may cause issues with your database column size. Before storing
	any encrypted data in your database, ensure that you have the proper
	column width otherwise you may experience truncation of your data depending
	on the database engine in use.

	To have the mixin enforce max field length, either:
		a) set ENFORCE_MAX_LENGTH = True in your settings files
		b) set 'enforce_max_length' to True in the kwargs of your model.

	A ValueError will be raised if the encrypted length of the data (including
	prefix if specified) is greater than the max_length of the field.
	"""

	if django.VERSION < (1, 8):
		__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		"""
		Initialize the EncryptedFieldMixin with the following optional settings:
		* key: The key to encrypt this field with.
		* crypter_class: A custom class that is extended from CryptoWrapper.
		* prefix: A static string prepended to all encrypted data.
		"""
		crypter_class = kwargs.pop('crypter_class', NaClWrapper)

		key = kwargs.pop('key', None)
		if not key:
			if hasattr(settings, 'ENCRYPTED_FIELDS_KEY'):
				key = settings.ENCRYPTED_FIELDS_KEY
			else:
				raise ImproperlyConfigured(
					'You must set settings.ENCRYPTED_FIELDS_KEY or name a key with '
					'kwarg `key`'
				)

		# Prefix encrypted data with a static string to allow filtering
		# of encrypted data vs. non-encrypted data using vanilla MySQL queries.
		self.prefix = kwargs.pop('prefix', '')

		self._crypter = crypter_class(key)

		# Ensure the encrypted data does not exceed the max_length
		# of the database. Data truncation is a possibility otherwise.
		self.enforce_max_length = kwargs.pop('enforce_max_length', False)
		if not self.enforce_max_length:
			self.enforce_max_length = getattr(
				settings,
				'ENCRYPTED_FIELDS_ENFORCE_MAX_LENGTH',
				False
			)

		super(EncryptedFieldMixin, self).__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'TextField'

	def from_db_value(self, value, expression, connection, context):
		if value is None or value == '' or not isinstance(value, str):
			return value

		# Remove prefix if it was prepended to the ciphertext.
		if self.prefix and value.startswith(self.prefix):
			value = value[len(self.prefix):]

		value = self._crypter.decrypt(value)
		value = value.encode().decode('unicode_escape')

		return super(EncryptedFieldMixin, self).to_python(value)

	def get_db_prep_value(self, value, connection, prepared=False):
		if value is None or value == '':
			return value

		if isinstance(value, str):
			value = value.encode('unicode_escape').decode()
			# value = value.encode('ascii').decode()
		else:
			value = str(value)

		value = self.prefix + self._crypter.encrypt(value)

		if self.enforce_max_length:
			if value and hasattr(self, 'max_length') and \
				self.max_length and self.max_length < len(value):
				raise ValueError(
					'Field {0} max_length={1} encrypted_len={2}'.format(
						self.name, self.max_length, len(value),
					)
				)

		return value


class EncryptedCharField(EncryptedFieldMixin, models.CharField):
	pass


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
	pass


class EncryptedDateTimeField(EncryptedFieldMixin, models.DateTimeField):
	pass


class EncryptedIntegerField(EncryptedFieldMixin, models.IntegerField):
	@cached_property
	def validators(self):
		"""
		See issue https://github.com/defrex/django-encrypted-fields/issues/7
		Need to keep all field validators, but need to change
		`get_internal_type` on the fly to prevent fail in django 1.7.
		"""
		self.get_internal_type = lambda: 'IntegerField'
		return models.IntegerField.validators.__get__(self)


class EncryptedDateField(EncryptedFieldMixin, models.DateField):
	pass


class EncryptedFloatField(EncryptedFieldMixin, models.FloatField):
	pass


class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
	pass


class EncryptedBooleanField(EncryptedFieldMixin, models.BooleanField):
	pass


try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^encrypted_fields\.fields\.\w+Field'])
except ImportError:
	pass
