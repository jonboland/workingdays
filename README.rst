Working Days
============

A command line application that takes a date and prints the number of working days left in the associated month.

.. code-block:: shell-session

 usage: calculate.py [-h] [-c COUNTRY] [-s SUBDIV] date

 Calculate the number of working days left in a month.

 positional arguments:
   date                  Date in DD/MM/YYYY format. The output from the program will be the number of working days left
                         in the month after the given date.

 options:
   -h, --help            show this help message and exit
   -c COUNTRY, --country COUNTRY
                         Name of country to base working day calculation on. Country names are specified using ISO
                         3166-1 alpha-2 codes, such as GB, US, CA, etc. Most countries can also be specified by name
                         (Canada, Turkey, etc.). (default: GB)
   -s SUBDIV, --subdiv SUBDIV
                         Name of country subdivision to base working day calculation on. Subdivisions are specified
                         using ISO 3166-2 codes, such as England, NY, ON, etc. For countries that don't have
                         subdivisions, use None. (default: England)
