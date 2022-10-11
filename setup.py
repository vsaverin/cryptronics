from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

setup(name='Cryptronics',
      version='0.1',
      description='Easy to use crypto API for python.',
      packages=['Cryptronics'],
      author_email='vasiliy.saverin@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)
