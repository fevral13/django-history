from setuptools import setup

setup(
    name='django-history',
    version='0.1',
    description="Model change logging",
    author='Serj Zavadsky',
    author_email='fevral13@gmail.com',
    url='https://github.com/fevral13/django-history',
    packages=['django_history', ],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
