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

from zc.buildout import easy_install

class Eggpaths(object):

    def __init__(self, buildout, name, options):
        """ Take the eggs we're given, and save the path to them into buildout variables """ 

        # set up some internal class stuff we'll need later
        self.buildout = buildout
        self.name = name
        self.options = options

        # get the list of eggs that was specified in the buildout part
        eggs = [x.strip() for x in self.options['eggs'].split('\n')]

        # get the directories that the eggs will be installed in from buildout
        egg_paths = [
            self.buildout["buildout"]["develop-eggs-directory"],
            self.buildout["buildout"]["eggs-directory"],
            ]

        # get the current working set of the eggs
        ws = easy_install.working_set(eggs, self.buildout['buildout']['executable'] ,egg_paths)

        # get the eggs we're interested in out of the working set
        self.eggs_of_interest = {}
        for egg in eggs:
            # get a dict of the egg names that have actually been installed against the paths used
            entry_names = {}
            for entry in ws.entries:
                entry_names[entry.split('/')[-1]] = entry

            # now we have the eggs names and paths that have been installed
            # check if they are actually of interest
            # by matching against the eggs that were specified in the buildout

            # egg paths are of the form Name-Version-PyVersion.
            # So, check that we are starting with the right name, and finishing in a -
            # Should give the name of the egg that was installed, so we can match against it
            self.eggs_of_interest[egg] = [entry_names[x] for x in entry_names.keys() if (x.lower().startswith(egg.lower() + '-') or (x.lower() == egg.lower()))][0]


        # now we've done that, set the buildout options we were after
        for key, value in self.eggs_of_interest.iteritems():
            self.options.setdefault(key, value)

    def install(self):
        """ Write out the paths that we've found to a handy text file """

        # get the directory to put the file in
        outputdir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)

        # create this directory
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        # write out the file
        out_file = open(os.path.join(outputdir, "eggpaths.txt"), 'w')

        for key, value in self.eggs_of_interest.iteritems():
            out_file.write(key + ': ' + value + '\n')

        # tidy up
        out_file.flush()
        out_file.close()

        # buildout expects paths that have been altered
        return outputdir



    def update(self):
        self.install()
