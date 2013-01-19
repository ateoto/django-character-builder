from setuptools import setup

version = __import__('character_builder').__version__

setup(name = 'django-character-builder',
    version = version,
    author = 'Matthew McCants',
    author_email = 'mattmccants@gmail.com',
    description = 'D&D Character Builder',
    license = 'BSD',
    url = 'https://github.com/Ateoto/django-character-builder',
    packages = ['character_builder'],
    install_requires = ['django>=1.4'])
