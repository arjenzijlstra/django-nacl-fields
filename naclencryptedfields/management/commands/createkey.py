
from django.core.management.base import BaseCommand
from encrypted_fields.backends import NaClWrapper

import base64


class Command(BaseCommand):
	help = 'Create a key for NaClWrapper.'

	def handle(self, *args, **options):
		key = NaClWrapper.createKey()
		print(key)
		bkey = base64.b64encode(key).decode('ascii')
		print('Put the following line in your settings.py:'
		      'NACL_FIELDS_KEY = \'%s\'' % base64.b64encode(key).decode('ascii'))
		print(base64.b64decode(bkey))
