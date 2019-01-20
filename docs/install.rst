============
Installation
============

Setups for setting up Sphinx

-------------------
Installing PlantUML
-------------------

| Install JAVA and Graphviz with ``brew install graphviz``
| Get plantuml.jar file from `plantuml site`_.
| Make /usr/local/bin/plantuml file

.. code-block:: bash

   #!/bin/sh -e
   java -jar /path/to/plantuml.jar "$@"

| Then chmod 755 the file


---------------
Running Locally
---------------

.. code-block:: bash

   cd PROJECT_ROOT
   python build_apispec.py
   sphinx-autobuild docs docs/_build/html

| ``sphinx-autobuild`` will rebuild the docs and refresh the browser whenever there is a change in the RST files
| To change the REST API specs, edit and rerun ``build_apispec.py``
| This will update /docs/apispec.json, which will then trigger ``sphinx-autobuild`` to rebuild the docs and refresh the browser

.. _plantuml site: http://sourceforge.net/projects/plantuml/files/plantuml.jar/download