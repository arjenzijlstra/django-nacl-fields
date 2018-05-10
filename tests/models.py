
from django.db import models

from encrypted_fields.fields import (
	EncryptedBooleanField,
	EncryptedCharField,
	EncryptedDateField,
	EncryptedDateTimeField,
	EncryptedEmailField,
	EncryptedFloatField,
	EncryptedIntegerField,
	EncryptedTextField,
)

from tests.backends.testcryptowrapper import TestCryptoWrapper


class TestModel(models.Model):
	boolean = EncryptedBooleanField(default=False, blank=True)
	char = EncryptedCharField(max_length=255, null=True, blank=True)
	date = EncryptedDateField(null=True, blank=True)
	datetime = EncryptedDateTimeField(null=True, blank=True)
	email = EncryptedEmailField(null=True, blank=True)
	floating = EncryptedFloatField(null=True, blank=True)
	integer = EncryptedIntegerField(null=True, blank=True)
	text = EncryptedTextField(null=True, blank=True)

	prefix_char = EncryptedCharField(
		max_length=255, prefix='ENCRYPTED:::', blank=True)
	short_char = EncryptedCharField(
		max_length=50, null=True, enforce_max_length=True, blank=True)

	custom_crypter_char = EncryptedCharField(
		max_length=255, null=True, crypter_class=TestCryptoWrapper, blank=True)
