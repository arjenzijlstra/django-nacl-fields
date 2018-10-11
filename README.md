# NaCl Encrypted Fields

This is a collection of Django Model Field classes that are encrypted using [PyNaCl](https://github.com/pyca/pynacl). This package is largely based on [django-encrypted-fields](https://github.com/defrex/django-encrypted-fields), which makes use of the outdated Keyczar library to encrypt fields. Besides that, it is inspired by [django-fernet-field](https://github.com/orcasgit/django-fernet-fields).


## About PyNaCl

[PyNaCl](https://github.com/pyca/pynacl) is a Python binding to (libsodium)[https://github.com/jedisct1/libsodium], which is a fork of the (Networking and Cryptography library)[https://nacl.cr.yp.to]. These libraries have a stated goal of improving usability, security and speed.


## Getting Started
TODO

```shell
~ pip install nacl-encrypted-fields
```

Create a key to be used for encryption.
```shell
~ python manage.py createkey
Put the following line in your settings.py:

NACL_FIELDS_KEY = 'cGa9QJDY/FJhbITXHnrIqlgyeLDS04/WqWtgqPEIU4A='
```

In your `settings.py`
```python
NACL_FIELDS_KEY = 'cGa9QJDY/FJhbITXHnrIqlgyeLDS04/WqWtgqPEIU4A='
```

Then, in your `models.py`
```python
from django.db import models
from naclencryptedfields import NaClEncryptedTextField


class MyModel(models.Model):
    text_field = NaClEncryptedTextField()
```

Use your model as normal and your data will be encrypted in the database.

**Note:** Encrypted data cannot be used to query or sort. In SQL, these will all look like text fields with random text.


## Available Fields

Currently build in and unit-tested fields.

-  `NaClEncryptedCharField`
-  `NaClEncryptedTextField`
-  `NaClEncryptedDateTimeField`
-  `NaClEncryptedIntegerField`
-  `NaClEncryptedFloatField`
-  `NaClEncryptedEmailField`
-  `NaClEncryptedBooleanField`


## Encrypt Your Own Fields

Making new fields can be done by using the build-in NaClEncryptedFieldMixin:
```python
from django.db import models
from naclencryptedfields import NaClEncryptedFieldMixin


class EncryptedIPAddressField(NaClEncryptedFieldMixin, models.IPAddressField):
    pass
```

Please report any issues you encounter when trying this.


## ToDo List

*  Add License
*  Add salt per field

## References

*  https://github.com/defrex/django-encrypted-fields
*  https://github.com/orcasgit/django-fernet-fields
