from setuptools import setup

version = __import__('ateoto_recipe').__version__

setup(name = 'django-ateoto-recipe',
    version = version,
    author = 'Matthew McCants',
    author_email = 'mattmccants@gmail.com',
    description = 'Recipe database for ateoto.com',
    license = 'BSD',
    url = 'https://github.com/Ateoto/django-ateoto-recipe',
    packages = ['ateoto_recipe'],
    install_requires = ['django>=1.4'])
