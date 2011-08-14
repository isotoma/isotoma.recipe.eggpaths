# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import logging

from zc.buildout import easy_install
from pkg_resources import to_filename

class Eggpaths(object):
    
    def foo(self, dist):
        print dist
        

    def __init__(self, buildout, name, options):
        """ Take the eggs we're given, and save the path to them into buildout variables """ 

        # set up some internal class stuff we'll need later
        self.buildout = buildout
        self.name = name
        self.options = options

        # check if we have versions information
        # if we don't, there's not a lot we can really do
        if not self.buildout['buildout'].has_key('versions'):
            # log and bail
            logging.error('Buildout does not have versions information')
            sys.exit(1)
        
        # get the versions section from buildout
        versions_name = self.buildout['buildout']['versions']
        versions_section = self.buildout[versions_name]
        
        # stick this in our local buildout space
        # we also need to add the path to the egg
        for k,v in versions_section.iteritems():
            egg_directory = self.buildout['buildout']['eggs-directory']
            python_version = '.'.join([str(x) for x in sys.version_info[0:2]])
            k = to_filename(k)
            v = to_filename(v)

            path_to_egg = os.path.join(egg_directory, k + '-' + v + '-py' + python_version +'.egg/')
            
            self.options.setdefault(k, path_to_egg)
        

    def install(self):
        """ Write out the paths that we've found to a handy text file """

        # get the directory to put the file in
        outputdir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)

        # create this directory
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        # write out the file
        out_file = open(os.path.join(outputdir, "eggpaths.txt"), 'w')

        for key, value in self.options.iteritems():
            out_file.write(key + ': ' + value + '\n')

        # tidy up
        out_file.flush()
        out_file.close()

        # buildout expects paths that have been altered
        return outputdir



    def update(self):
        self.install()
