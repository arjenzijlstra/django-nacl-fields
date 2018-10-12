
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': ':memory:',
	},
}

SECRET_KEY = 'jw1fk!h%v#b4&-+2wq5d6v#$4@u1-lh+(i)kxj--7pw7!59&r+'

INSTALLED_APPS = (
	'tests',
	'naclencryptedfields'
)

MIDDLEWARE_CLASSES = []

NACL_FIELDS_KEY = 'Y4/g/BYl7GicK7Vqz4nnf2ziB+cv80FQl8gxFxWRdZU='
