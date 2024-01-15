import sys
from admin_honeypot import __version__, __description__, __license__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='django-admin-honeypot-1.2.0',
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django admin honeypot trap',
    maintainer='Kalyaan Singh',
    maintainer_email='kalyaanks075@gmail.com',
    # url='https://github.com/dmpayton/django-admin-honeypot',
    # download_url='https://github.com/dmpayton/django-admin-honeypot/tarball/v%s' % __version__,
    license=__license__,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
)
