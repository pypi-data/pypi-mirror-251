from distutils.core import setup

setup(
    packages=['SambdaTester'],
    entry_points = {
        'console_scripts': [
            'doItLive=doItLive:main',
            'bin/doIt=doItLive.command:main'
        ]
    },
    author_email = "tarnold0788@gmail.com"
)
