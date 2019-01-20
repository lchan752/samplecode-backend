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

----------------
Database Diagram
----------------

.. uml::

   @startuml
   left to right direction
   class User {
     id: int
     name: string
   }

   class Address {
     id: int
     user_id: int
     line1: string
     line2: string
     city: string
   }

   class Phone {
     id: int
     user_id: int
     phone_number: string
     phone_type: string
   }

   User::id <-- Address::user_id : 1 to many
   User::id <-- Phone::user_id : 1 to many
   @enduml

.. _PlantUML: http://plantuml.com/