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
import pkg_resources

from zc.buildout import easy_install, UserError
from zc.recipe.egg import Eggs

class Eggpaths(object):

    def __init__(self, buildout, name, options):
        self.eggs = Eggs(buildout, name, options)
        self.buildout = buildout
        self.name = name
        self.options = options
        self.log = logging.getLogger(__name__)

        egg_list =  [s.strip() for s
                    in self.options.get('eggs', '').splitlines()
                    if s.strip()]

        requirements, ws = self.eggs.working_set(egg_list)

        for egg_name in egg_list:
            requirement = pkg_resources.Requirement.parse(egg_name)
            package = ws.find(requirement)
            if package:
                self.log.debug('%s = %s' % (requirement, package.location))
                self.options.setdefault(egg_name, package.location)
            else:
                raise UserError('Cannot locate the egg path for %s' % egg_name)

    def install(self):
        return ()

    update = install
