
from django.core.management.base import BaseCommand
from naclencryptedfields.backends import NaClWrapper


class Command(BaseCommand):
	help = 'Create a key for NaClWrapper.'

	def handle(self, *args, **options):
		key = NaClWrapper.createKey()
		print('# put the following line in your settings.py\n'
		      'NACL_FIELDS_KEY = \'%s\'' % key)
