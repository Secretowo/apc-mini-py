from setuptools import setup

setup(
    name='akai_pro_py',
    version='0.2.3',
    description='A simple library for interfacing with the Akai Professional series of MIDI controllers',
    url='https://github.com/Secretowo/apc-mini-py',
    author='Secret and Lewis L. Foster',
    author_email='Secret <unknown>, Lewis L. Foster <lewis@sniff122.tech>',
    license='',
    packages=['akai_pro_py'],
    install_requires=['mido',
                      'asyncio',
                      'python-rtmidi'
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',

    ],
)
