from setuptools import setup, find_packages

setup(
    name='mtvc-api-client',
    version='0.0.13',
    description='Praekelt MTVC API Client',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/mtvc-api-client',
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        'hammock==0.2.4'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
