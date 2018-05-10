
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': ':memory:',
	},
}

SECRET_KEY = 'r4nD0Mp4sSw0rD'

INSTALLED_APPS = (
	'tests',
	'encrypted_fields'
)

MIDDLEWARE_CLASSES = []

# ENCRYPTED_FIELDS_KEY = 0x638fe0fc1625ec689c2bb56acf89e77f6ce207e72ff3415097c8311715917595
# ENCRYPTED_FIELDS_KEY = b'Y4/g/BYl7GicK7Vqz4nnf2ziB+cv80FQl8gxFxWRdZU='
ENCRYPTED_FIELDS_KEY = b'\xfa\xe0@\x9e\xbc\x9cB\x92\x82\xf2\xb7F\xf7\xc3$\x02\xc90\x83\xe2B\tH\xf9\x8a\x11\xec\x06{\xe1_\x91'
