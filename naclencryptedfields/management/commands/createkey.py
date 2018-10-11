
from django.core.management.base import BaseCommand
from naclencryptedfields.backends import NaClWrapper

import base64


class Command(BaseCommand):
	help = 'Create a key for NaClWrapper.'

	def handle(self, *args, **options):
		key = NaClWrapper.createKey()
		bkey = base64.b64encode(key).decode('ascii')
		print('Put the following line in your settings.py:\n\n'
		      'NACL_FIELDS_KEY = \'%s\'\n' % base64.b64encode(key).decode('ascii'))
