from setuptools import setup, find_packages

setup(
    name='mtvc-api-client',
    version='0.0.1',
    description='Praekelt MTVC API Client',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/mtvc-api-client',
    packages = find_packages(),
    dependency_links = [],
    install_requires = [
        'hammock==0.2.4'
    ],
    include_package_data=True,
    zip_safe=False,
)