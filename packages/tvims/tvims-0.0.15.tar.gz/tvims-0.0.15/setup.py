from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='tvims',
    version='0.0.15',
    description='Aboubakar',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='tak0ysebe',
    author_email='ffmarkov@yandex.ru',
    classifiers=classifiers,
    license='MIT',
    include_package_data=True,  # Include data files specified in MANIFEST.in
    
    package_data={
        '': ['pic/*.png'],  # Include all PNG files in the 'pic' directory
    },
    keywords='test',
    packages=find_packages(),
    install_requiers=['']

)
