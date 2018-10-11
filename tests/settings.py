
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': ':memory:',
	},
}

SECRET_KEY = 'r4nD0Mp4sSw0rD'

INSTALLED_APPS = (
	'tests',
	'naclencryptedfields'
)

MIDDLEWARE_CLASSES = []

NACL_FIELDS_KEY = b'Y4/g/BYl7GicK7Vqz4nnf2ziB+cv80FQl8gxFxWRdZU='
