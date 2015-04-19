from pkg_resources import parse_version
from setuptools import setup, find_packages

cgcloud_version = '1.0.dev1'

dependency_links = [ ]


def add_private_dependency( name, version=cgcloud_version, git_ref=None ):
    if git_ref is None:
        git_ref = 'master' if parse_version( version ).is_prerelease else version
    url = 'git+https://github.com/BD2KGenomics'
    dependency_links.append(
        '{url}/{name}.git@{git_ref}#egg={name}-{version}'.format( **locals( ) ) )
    return '{name}=={version}'.format( **locals( ) )


setup(
    name='cgcloud-core',
    version=cgcloud_version,

    author='Hannes Schmidt',
    author_email='hannes@ucsc.edu',
    url='https://github.com/BD2KGenomics/cgcloud-core',
    description='Efficient and reproducible software deployment for EC2 instances',

    package_dir={ '': 'src' },
    packages=find_packages( 'src', exclude=[ '*.test' ] ),
    namespace_packages=[ 'cgcloud' ],
    entry_points={
        'console_scripts': [
            'cgcloud = cgcloud.core.ui:main' ], },
    install_requires=[
        add_private_dependency( 'bd2k-python-lib', '1.5' ),
        add_private_dependency( 'cgcloud-lib' ),
        'pkginfo>=1.1',
        'boto>=2.36.0',
        'Fabric>=1.7.0',
        'PyYAML>=3.10' ],
    setup_requires=[
        'nose>=1.3.4' ],
    dependency_links=dependency_links,
    test_suite='cgcloud.core.test' )
