import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
        Description: Load each table using the queries in `copy_table_queries` list.
        Arguments:
            cur: the cursor object. 
            conn: connection to the database.
        Returns:
            None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
        Description: Inserts each table using the queries in `insert_table_queries` list.
        Arguments:
            cur: the cursor object. 
            conn: connection to the database.
        Returns:
            None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Read the dwh.cfg configuration file
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Load staging tables.
    
    - Insert into all tables.
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()