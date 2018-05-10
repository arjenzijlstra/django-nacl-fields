# -*- coding: utf-8 -*-

import re
import unittest

import django
from django.conf import settings
from django.db import connection
from django.test import TestCase
from django.utils import timezone

from tests.models import TestModel
from tests.backends.testcryptowrapper import TestCryptoWrapper


class FieldsTest(TestCase):
	IS_POSTGRES = settings.DATABASES['default']['ENGINE'] == \
		'django.db.backends.postgresql_psycopg2'

	def get_db_value(self, field, model_id):
		cursor = connection.cursor()
		cursor.execute(
			'select {0} from tests_testmodel where id = {1};'.format(field, model_id)
		)
		return cursor.fetchone()[0]

	def test_char_field_encrypted_custom(self):
		plaintext = 'Oh hi, test reader!'

		model = TestModel()
		model.custom_crypter_char = plaintext
		model.save()

		ciphertext = self.get_db_value('custom_crypter_char', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('test' not in ciphertext)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.custom_crypter_char, plaintext)

	def test_prefix_char_field_encrypted(self):
		plaintext = 'Oh hi, test reader!'

		model = TestModel()
		model.prefix_char = plaintext
		model.save()

		ciphertext = self.get_db_value('prefix_char', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('test' not in ciphertext)
		self.assertTrue(ciphertext.startswith('ENCRYPTED:::'))

	def test_char_field_encrypted(self):
		plaintext = 'Oh hi, test reader!'

		model = TestModel()
		model.char = plaintext
		model.save()

		ciphertext = self.get_db_value('char', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('test' not in ciphertext)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.char, plaintext)

	def test_unicode_encrypted(self):
		plaintext = u'Oh hi, test reader! 🐱'

		model = TestModel()
		model.char = plaintext
		model.save()

		ciphertext = self.get_db_value('char', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('test' not in ciphertext)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.char, plaintext)

	def test_short_char_field_encrypted(self):
		""" Test the max_length validation of an encrypted char field """
		plaintext = 'Oh hi, test reader!'

		model = TestModel()
		model.short_char = plaintext
		self.assertRaises(ValueError, model.save)

	def test_text_field_encrypted(self):
		plaintext = 'Oh hi, test reader!' * 10

		model = TestModel()
		model.text = plaintext
		model.save()

		ciphertext = self.get_db_value('text', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('test' not in ciphertext)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.text, plaintext)

	def test_datetime_field_encrypted(self):
		plaintext = timezone.now()

		model = TestModel()
		model.datetime = plaintext
		model.save()

		ciphertext = self.get_db_value('datetime', model.id)

		# Django's normal date serialization format
		self.assertTrue(re.search('^\d\d\d\d-\d\d-\d\d', ciphertext) is None)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.datetime, plaintext)

	def test_integer_field_encrypted(self):
		plaintext = 42

		model = TestModel()
		model.integer = plaintext
		model.save()

		ciphertext = self.get_db_value('integer', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertNotEqual(plaintext, str(ciphertext))

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.integer, plaintext)

	def test_date_field_encrypted(self):
		plaindate = timezone.now().date()

		model = TestModel()
		model.date = plaindate
		model.save()

		ciphertext = self.get_db_value('date', model.id)
		fresh_model = TestModel.objects.get(id=model.id)

		self.assertNotEqual(ciphertext, plaindate.isoformat())
		self.assertEqual(fresh_model.date, plaindate)

	def test_float_field_encrypted(self):
		plaintext = 42.44

		model = TestModel()
		model.floating = plaintext
		model.save()

		ciphertext = self.get_db_value('floating', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertNotEqual(plaintext, str(ciphertext))

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.floating, plaintext)

	def test_email_field_encrypted(self):
		plaintext = 'aron.jones@gmail.com'  # my email address, btw

		model = TestModel()
		model.email = plaintext
		model.save()

		ciphertext = self.get_db_value('email', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertTrue('aron' not in ciphertext)

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.email, plaintext)

	def test_boolean_field_encrypted(self):
		plaintext = True

		model = TestModel()
		model.boolean = plaintext
		model.save()

		ciphertext = self.get_db_value('boolean', model.id)

		self.assertNotEqual(plaintext, ciphertext)
		self.assertNotEqual(True, ciphertext)
		self.assertNotEqual('True', ciphertext)
		self.assertNotEqual('true', ciphertext)
		self.assertNotEqual('1', ciphertext)
		self.assertNotEqual(1, ciphertext)
		self.assertTrue(not isinstance(ciphertext, bool))

		fresh_model = TestModel.objects.get(id=model.id)
		self.assertEqual(fresh_model.boolean, plaintext)

	@unittest.skipIf(django.VERSION < (1, 7), "Issue exists in django 1.7+")
	@unittest.skipIf(not IS_POSTGRES, "Issue exists for postgresql")
	def test_integerfield_validation_in_django_1_7_passes_successfully(self):
		plainint = 1111

		obj = TestModel()
		obj.integer = plainint

		# see https://github.com/defrex/django-encrypted-fields/issues/7
		obj.full_clean()
		obj.save()

		ciphertext = self.get_db_value('integer', obj.id)

		self.assertNotEqual(plainint, ciphertext)
		self.assertNotEqual(plainint, str(ciphertext))

		fresh_model = TestModel.objects.get(id=obj.id)
		self.assertEqual(fresh_model.integer, plainint)
