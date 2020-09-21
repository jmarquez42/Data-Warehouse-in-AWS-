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

Consultation to validate the load.
> ` SELECT a.name as Artists, s.title as Songs, COUNT(1) AS NumberReproductions
FROM songplays sp JOIN artists a ON sp.artist_id = a.artist_id
JOIN songs s ON sp.song_id = s.song_id
GROUP BY a.name, s.title
ORDER BY numberReproductions DESC
LIMIT 5`

<table>
				<tbody>
					<tr>
						<td>artists</td>
						<td>songs</td>
						<td>numberreproductions</td>
					</tr>
					<tr>
						<td>Dwight Yoakam</td>
						<td>You&#39;re The One</td>
						<td>37</td>
					</tr>
					<tr>
						<td>Ron Carter</td>
						<td>I CAN&#39;T GET STARTED</td>
						<td>9</td>
					</tr>
					<tr>
						<td>Lonnie Gordon</td>
						<td>Catch You Baby (Steve Pitron &amp; Max Sanna Radio Edit)</td>
						<td>9</td>
					</tr>
					<tr>
						<td>B.o.B</td>
						<td>Nothin&#39; On You [feat. Bruno Mars] (Album Version)</td>
						<td>8</td>
					</tr>
					<tr>
						<td>Usher</td>
						<td>Hey Daddy (Daddy&#39;s Home)</td>
						<td>6</td>
					</tr>
				</tbody>
	</table>


## Authors

* **Jose Marquez** - [Github](https://github.com/jmarquez42)
    

