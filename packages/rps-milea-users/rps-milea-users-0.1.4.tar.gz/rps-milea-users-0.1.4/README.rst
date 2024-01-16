===========================
Django E-Mail User
===========================

Just another Django-email-user app. Makes the email address as the username.

Attention! Only suitable for fresh Django projects.


Installation
============

* Installation ::

    pip install rps-milea-users


* Add ``rps_milea_users`` to ``INSTALLED_APPS`` in settings.py ::

    INSTALLED_APPS = [
      "rps_milea_users",
      ...
    ]

* Create ``AUTH_USER_MODEL`` in settings.py ::

    AUTH_USER_MODEL = 'rps_milea_users.User'

* Database Update ::

    python manage.py migrate


Internal Notes
==============

Publishing to PyPI::

	python -m pip install -U wheel twine setuptools
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload --skip-existing dist/*
