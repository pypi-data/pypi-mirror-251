from setuptools import setup

setup(
    name='olxApi',
    version='0.2.1',
    py_modules=['olxapi'],
    description='A simple OLX scraper module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kleber Coelho',
    author_email='kleber.amg79@gmail.com',
    url='https://github.com/kcoelho79/OLXApi',
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    python_requires='>=3.6',
)
