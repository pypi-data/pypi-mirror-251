from setuptools import setup, find_packages

setup(
    name='tiberlogger',
    use_scm_version=True,  # Enable setuptools_scm for versioning
    setup_requires=['setuptools_scm'],  # Add setuptools_scm as a setup requirement
    packages=find_packages(),
    url='https://github.com/tiberhealth/TiberLogger',
    license='',
    author='Tiber Health Innovations',
    author_email='tiber-tools@tiberhealth.com',
    description='Common logging routine for Tiber Health Python  scripts and appplications',
    long_description='Tiber Logger is a common Python package to assist with a common logging routine for Tiber Health scripts and applications',
    install_requires=[]
)
