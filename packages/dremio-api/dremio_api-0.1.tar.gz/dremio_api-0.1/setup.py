from setuptools import setup

setup(name='dremio_api',
      version='0.1',
      packages=['dremio_api'],
      zip_safe=False,
      # dependencies
      install_requires=[
          'pandas',
          'pyarrow>=11.0.0',
          'certifi',
      ]
      )