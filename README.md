dbmonitor
=========

DB monitor Tool for Oracle, MySQL and PostgreSQL


Simple app that monitors connections, long running queries and locks in different databases.
This project probably has no useful purpose. I simply decided to learn python and this seemed like a good place to start. 


How to run:

For ORACLE Databases an Instant Client instalation is required, with corresponding tnsname.ora file.
You also require the $ORACLE_HOME env variable and the $ORACLE_HOME/lib in your LD_LIBRARY_PATH.

You can then execute the script as:

  ./main.py -t Oracle -u username -p password -n ConnectionID
  
  

For MySQL databases you can execute the script with:

./main.py -t MySQL -u username -p password -d databasename -s server
  
