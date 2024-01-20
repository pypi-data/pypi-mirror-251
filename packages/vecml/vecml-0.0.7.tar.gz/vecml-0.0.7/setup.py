from setuptools import setup

setup(name='vecml',
      version='0.0.7',
      description='The VecML client',
      url='https://www.vecml.com',
      author='VecML Inc',
      author_email='support@vecml.com',
      license='Apache-2.0',
      packages=['vecml'],
      install_requires=[
        'grpcio',
        'numpy',
        'scipy',
        'tqdm',
        'protobuf'
      ],
      zip_safe=False)
