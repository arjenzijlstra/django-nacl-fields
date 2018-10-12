
from django.db import models

from naclencryptedfields.fields import (
	NaClEncryptedBooleanField,
	NaClEncryptedCharField,
	NaClEncryptedDateField,
	NaClEncryptedDateTimeField,
	NaClEncryptedEmailField,
	NaClEncryptedFloatField,
	NaClEncryptedIntegerField,
	NaClEncryptedTextField,
)

from tests.backends.testcryptowrapper import TestCryptoWrapper


class TestModel(models.Model):
	boolean = NaClEncryptedBooleanField(default=False, blank=True)
	char = NaClEncryptedCharField(max_length=255, null=True, blank=True)
	date = NaClEncryptedDateField(null=True, blank=True)
	datetime = NaClEncryptedDateTimeField(null=True, blank=True)
	email = NaClEncryptedEmailField(null=True, blank=True)
	floating = NaClEncryptedFloatField(null=True, blank=True)
	integer = NaClEncryptedIntegerField(null=True, blank=True)
	text = NaClEncryptedTextField(null=True, blank=True)

	custom_crypto_char = NaClEncryptedCharField(
		max_length=255, null=True, crypto_class=TestCryptoWrapper, blank=True)
