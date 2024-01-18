from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='MayakApiClient_test_1',
  version='0.0.3',
  author='mr360',
  author_email='vadgr1schin@yandex.ru',
  description='This is the simplest module for quick work with files.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  # url='your_url',
  packages=find_packages(),
  install_requires=[
    'anyio==4.2.0', 'certifi==2023.11.17', 'charset-normalizer==3.3.2',
    'dadata==21.10.1', 'greenlet==3.0.3',
    'h11==0.14.0', 'httpcore==1.0.2', 'httpx==0.26.0',
    'idna==3.6', 'numpy==1.26.3', 'pandas==2.1.4', 'pillow==10.2.0',
    'python-dateutil==2.8.2', 'pytz==2023.3.post1', 'requests==2.31.0',
    'six==1.16.0', 'sniffio==1.3.0',
    'SQLAlchemy==2.0.25', 'typing_extensions==4.9.0',
    'tzdata==2023.4', 'urllib3==2.1.0'
                    ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='mayak_api_test',
  # project_urls={
  #   'GitHub': 'your_github'
  # },
  python_requires='>=3.9'
)