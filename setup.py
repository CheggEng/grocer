from setuptools import setup

setup(
    name='grocer',
    version='1.0',
    packages=['grocer', 'grocer.lib'],
    url='',
    license='Apache 2.0',
    author='William Jimenez',
    author_email='wjimenez@chegg.com',
    description='Tools to manage ingredients for Chef',
    zip_safe=False,
    entry_points={
        'console_scripts': ['grocer_upload=grocer.grocer_upload:main',
                            'grocer_test=grocer.grocer_test:main']},
    install_requires=['argparse'],
)