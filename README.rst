Eggpaths buildout recipe
========================

This package provides a buildout_ recipe to get the paths to the eggs that have been installed. This is useful for referencing paths within an egg in a later buildout part, such as Apache aliases to a Django media directory.

The values are provided as buildout parameters in the section of which this is the recipe.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


For example::

  [eggpaths]
  recipe = isotoma.recipe.eggpaths
  eggs = Nose
         Django

  [apache]
  recipe = isotoma.recipe.apache
  aliases = /media:${eggpaths:Django}/contrib/admin/media


This recipe will also create a text file called eggpaths.txt in the parts directory, which can be used for reference

Mandatory parameters
--------------------

eggs
    The list of eggs that you are interested in the paths for


License
-------

Copyright 2010 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License.
