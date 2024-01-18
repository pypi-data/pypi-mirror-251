from setuptools import setup, find_packages

setup(name="demch_chat_client",
      version="0.0.2",
      description="demch_chat_client",
      author="Denis Demchenko",
      author_email="demchenkodenis1@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
