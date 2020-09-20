# Data Warehouse in AWS (Redshift)

The project consists of creating a data warehouse on AWS. 

## Project structure

Project files:

* ***dwh.cfg***: Configuration file.

* ***sql_queries.py***: Contains SQL statements for creating tables, dropping tables, inserting data, and selecting data.

* ***create_tables.py***: Contains the process that will generate the structure in the database from the instructions configured in the sql_queries.py file

* ***etl.py***: It is the process in ingesting the data.

* ***README.md***: This file contains the description of the project.

## Getting Started

### Prerequisites
<ul>
<li>Start a cluster in Redshift with the following features:
    <ul>
        <li>CLUSTER_TYPE: multi-node</li>
        <li>NUM_NODES: 2</li>
        <li>NODE_TYPE: dc2.large</li>
    </ul>
</li>
<li>The following libraries are required
    <ul>
        <li>Python 3.6.3</li>
        <li>Boto3  1.9.7</li>
        <li>Psycopg2 2.7.4</li>
    </ul>
</li>
<li>
Fill in the configuration file
</li> 
</ul>

### Installing.

1. Execute the following command to create the database structure.

> ` pytho.n create_tables.py; echo $?`

2. Execute the following command to perform the ingestion.

> `python etl.py; echo $?`

***If the program ends with 0 it was executed correctly.***

## Running the tests

To validate the ingest, you can run the queries in the test.ipynb file.

## Authors

* **Jose Marquez** - [Github](https://github.com/jmarquez42)
    

