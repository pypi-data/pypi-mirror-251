from setuptools import setup, find_packages

setup(name="den_chat_server",
      version="0.0.1",
      description="den_chat_server",
      author="Denis Demchenko",
      author_email="demchenkodenis1@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
