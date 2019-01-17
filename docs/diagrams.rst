===============
Making Diagrams
===============

Make diagrams with PlantUML_

-----------------
Activity Diagrams
-----------------

.. uml::

   @startuml
   start

   if (Graphviz installed?) then (yes)
   :process all\ndiagrams;
   else (no)
   :process only
   __sequence__ and __activity__ diagrams;
   endif

   stop
   @enduml

---------------
Object Diagrams
---------------

.. uml::

   @startuml
   left to right direction

   object user {
     name = "Dummy"
     id = 123
   }

   object address {
     flat = "10A"
     street = "Sesame Street"
     city = "New York"
   }

   user -- address: 1-to-Many

   @enduml

----------------
Usecase Diagrams
----------------

.. uml::

   @startuml
   left to right direction
   skinparam packageStyle rectangle
   actor customer
   actor clerk
   rectangle checkout {
     customer -- (checkout)
     (checkout) .> (payment) : include
     (help) .> (checkout) : extends
     (checkout) -- clerk
   }
   @enduml

.. _PlantUML: http://plantuml.com/