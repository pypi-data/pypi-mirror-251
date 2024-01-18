from setuptools import setup

setup(name='ml_wac',
      version='0.1',
      description='A Machine Learning Web-based Attack Classifier to detect and identify LFI, RFI, SQLI, and XSS attacks using the request paths',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/izak0s/ml_wac/',
      author='Jord & Isaac',
      author_email='ml_wac@izak.dev',
      license='GPLv3',
      packages=['ml_wac'],
      install_requires=['scikit-learn==1.2.2', 'xgboost', 'numpy'])