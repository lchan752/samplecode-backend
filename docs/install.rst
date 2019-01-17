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
   sphinx-autobuild docs docs/_build/html

Docs in browser will refresh whenever a change is made in the code

.. _plantuml site: http://sourceforge.net/projects/plantuml/files/plantuml.jar/download