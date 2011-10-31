from setuptools import setup, find_packages

version = '0.1.1'

setup(
    name = 'isotoma.recipe.eggpaths',
    version = version,
    description = "Get the paths to certain eggs that have been installed, so they can be referenced in other buildout sections",
    long_description = open("README.rst").read() + "\n" + \
                       open("CHANGES.txt").read(),
    classifiers = [ 
        "Framework :: Buildout",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
    ],  
    keywords = "buildout",
    author = "Tom Wardill",
    author_email = "tom.wardill@isotoma.com",
    license = "Apache Software License",
    url = "http://pypi.python.org/pypi/isotoma.recipe.eggpaths",
    packages = find_packages(exclude=['ez_setup']),
    package_data = { 
        '': ['README.rst', 'CHANGES.txt'],
    },  
    namespace_packages = ['isotoma', 'isotoma.recipe'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [ 
        'setuptools',
        'zc.buildout',
        'zc.recipe.egg',
    ],  
    entry_points = { 
        "zc.buildout": [
            "default = isotoma.recipe.eggpaths:Eggpaths",
        ],  
    }   
)

