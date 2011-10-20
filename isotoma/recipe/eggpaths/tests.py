import unittest
import tempfile
import shutil
import os, sys
import textwrap

from isotoma.recipe.eggpaths import Eggpaths
from zc.buildout import UserError

class TestEggpaths(unittest.TestCase):

    def setUp(self):
        self.tmpdirs = []

    def fake_buildout(self):
        ''' Create a fake buildout containing enough to satisfy zc.recipe.egg '''
        buildout_dir = tempfile.mkdtemp()

        test_egg_dir = tempfile.mkdtemp(dir=buildout_dir)
        test_develop_dir = tempfile.mkdtemp(dir=buildout_dir)
        test_bin_dir = tempfile.mkdtemp(dir=buildout_dir)

        self.tmpdirs.append(buildout_dir)

        return {
            'buildout': {
                'bin-directory': test_bin_dir,
                'eggs-directory': test_egg_dir,
                'executable': '/usr/bin/python',
                'versions': 'versions',
                'python': 'buildout',
                'develop-eggs-directory': test_develop_dir,
                'parts': '',
                'newest': 'true',
                'directory': buildout_dir,
                'develop': '',
                'offline': 'false',
                'eggs': '\nisotoma.recipe.eggpaths',
                'parts-directory': buildout_dir,
            },
            'versions': {}
        }

    def tearDown(self):
        for tmpdir in self.tmpdirs:
            shutil.rmtree(tmpdir)

    def egg_folder_eggs(self, egg_dir):
        return [
            os.path.join(egg_dir, eggpath)
            for eggpath in os.listdir(egg_dir)
        ]

    def build_develop_egg(self, egg_name, buildout_dir):
        ''' Build a temporary develop egg '''

        setup_config = textwrap.dedent('''
            from setuptools import setup, find_packages
            setup(
                name=%(egg_name)s,
                version='0.0.1',
                packages=find_packages(),
            )
        ''' % {'egg_name': egg_name})

        develop_dir = tempfile.mkdtemp(dir=buildout_dir)
        setup_file = open(os.path.join(develop_dir, 'setup.py'), 'w')
        setup_file.write(setup_config)
        setup_file.close()

        develop_egg_package = os.path.join(develop_dir, egg_name)
        os.mkdir(develop_egg_package)

        package_init= open(
            os.path.join(develop_egg_package, '__init__.py'), 'w'
        )
        package_init.write('print "Hello, world"')
        package_init.close()

        return develop_dir

    def test_simple_egg_path(self):
        ''' Test that the eggpath is present and correct '''
        buildout = self.fake_buildout()
        ep = Eggpaths(buildout, None, {
            'eggs': 'isotoma.recipe.apache',
        })
        ep.install()
        self.assertEqual(
            ep.options['isotoma.recipe.apache'] in self.egg_folder_eggs(
                buildout['buildout']['eggs-directory']
            ), True
        )

    def test_develop_egg(self):
        ''' Test that develop eggs are used where present '''
        buildout = self.fake_buildout()
        develop_egg_dir = self.build_develop_egg(
            'atestegg',
            buildout['buildout']['directory']
        )
        print >>sys.stderr, develop_egg_dir
        buildout['buildout']['develop'] = develop_egg_dir

        ep = Eggpaths(buildout, None, {
            'eggs': 'atestegg',
        })
        ep.install()
        self.assertEqual(ep.options['atestegg'], develop_egg_dir)
