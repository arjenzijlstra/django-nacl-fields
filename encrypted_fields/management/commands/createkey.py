
from django.core.management.base import BaseCommand
from encrypted_fields.backends import NaClWrapper

import base64


class Command(BaseCommand):
    help = 'Create a key for NaClWrapper.'

    def handle(self, *args, **options):
        key = NaClWrapper.createKey()
        # print('0x' + key.hex())
        # print(base64.b64encode(key))
        print(key)
