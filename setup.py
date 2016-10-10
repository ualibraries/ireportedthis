from setuptools import setup, find_packages
from src.ireportedthis import __version__

setup(

    name                 = 'ireportedthis',
    version              = __version__,
    packages             = find_packages( 'src' ),
    package_dir          = { '': 'src' },
    entry_points = {
    },

    install_requires     = [ 'requests', 'PyYAML', 'altair' ],

    author               = 'Mike Simpson',
    author_email         = 'mgsimpson@email.arizona.edu',
    description          = 'Quick and dirty IDoneThis report generator, highly opinionated.',
    license              = 'BSD 2-Clause',
    url                  = 'https://github.com/ualibraries/ireportedthis',

    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
)
