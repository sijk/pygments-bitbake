from setuptools import setup

setup(
    name = "pygments-bitbake",
    version = "1.0.0",
    license = "BSD",
    author = "Simon Knopp",
    author_email = "simon.knopp@pg.canterbury.ac.nz",
    url = "https://github.com/sijk/pygments-bitbake",
    description = "Pygments lexer for BitBake files.",
    long_description = open('README.rst').read(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],

    install_requires = ["pygments"],
    entry_points = {'pygments.lexers': 'bitbake = bitbake:BitbakeLexer'},

    py_modules = ["bitbake"],
)
