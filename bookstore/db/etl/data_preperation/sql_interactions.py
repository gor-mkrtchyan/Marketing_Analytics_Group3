"""
sql_interactions.py

This module provides a SqlHandler class for handling SQLite database operations, including insertion, retrieval,
and updates. It also includes methods for truncating and dropping database tables.

Author: Group 3
Date: November 17, 2023
"""


import sqlite3
import logging 
import pandas as pd
import numpy as np
import os
from bookstore.db.etl.logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class SqlHandler:
    """A class for handling SQLite database operations."""

    def __init__(self, dbname:str,table_name:str) -> None:
        """
        Initialize the SqlHandler object.

        Args:
            dbname (str): The name of the SQLite database.
            table_name (str): The name of the table within the database.
        """

        self.cnxn=sqlite3.connect(f'{dbname}.db')
        self.cursor=self.cnxn.cursor()
        self.dbname=dbname
        self.table_name=table_name

    def close_cnxn(self)->None:
        """Close the database connection."""

        logger.info('commiting the changes')
        self.cursor.close()
        self.cnxn.close()
        logger.info('the connection has been closed')

    def insert_one(self, data: pd.Series) -> None:
        """Insert a single row of data into the database.

        :param data: The data to be inserted as a Pandas Series.
        :type data: pd.Series
        :param data: pd.Series: 

        """
        # Check if the data Series contains the required columns
        if not set(data.index).issubset(self.get_table_columns()):
            logger.error("Data contains columns not present in the database table.")
            return

        # Ensure all values are non-null
        data = data.fillna(None)

        # Prepare a tuple for insertion
        values = tuple(data[column.lower()] for column in self.get_table_columns())

        # Define the SQL query for inserting a single row
        query = f"INSERT INTO your_table ({', '.join(self.get_table_columns())}) VALUES ({', '.join(['?'] * len(self.get_table_columns()))})"

        # Execute the query
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def get_table_columns(self)->list:
        """Retrieve the columns of the database table.


        :returns: The list of column names.

        :rtype: list

        """

        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        # self.cursor.close()

        return column_names
    
    def truncate_table(self)->None:
        """Truncate the database table."""

        query=f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        # self.cursor.close()

    def drop_table(self):
        """Drop the database table."""

        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)

        self.cursor.execute(query)

        self.cnxn.commit()

        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')

    def insert_many(self, df:pd.DataFrame) -> str:
        """Insert multiple rows of data into the database.

        :param df: The DataFrame containing the data to be inserted.
        :type df: pd.DataFrame
        :param df:pd.DataFrame: 
        :returns: A message indicating the status of the data loading.
        :rtype: str

        """

        df=df.replace(np.nan, None) # for handling NULLS
        df.rename(columns=lambda x: x.lower(), inplace=True)
        columns = list(df.columns)
        logger.info(f'BEFORE the column intersection: {columns}')
        sql_column_names = [i.lower() for i in self.get_table_columns()]
        columns = list(set(columns) & set(sql_column_names))
        logger.info(f'AFTER the column intersection: {columns}')
        ncolumns=list(len(columns)*'?')
        data_to_insert=df.loc[:,columns]
    
        values=[tuple(i) for i in data_to_insert.values]
        logger.info(f'the shape of the table which is going to be imported {data_to_insert.shape}')
        # if 'geometry' in columns: #! This block is usefull in case of geometry/geography data types
        #     df['geometry'] = df['geometry'].apply(lambda geom: dumps(geom))
        #     ncolumns[columns.index('geometry')]= 'geography::STGeomFromText(?, 4326)'
        
        if len(columns)>1:
            cols,params =', '.join(columns), ', '.join(ncolumns)
        else:
            cols,params =columns[0],ncolumns[0]
            
        logger.info(f'insert structure: colnames: {cols} params: {params}')
        logger.info(values[0])
        query=f"""INSERT INTO  {self.table_name} ({cols}) VALUES ({params});"""
        
        logger.info(f'QUERY: {query}')

        self.cursor.executemany(query, values)
        try:
            for i in self.cursor.messages:
                logger.info(i)
        except:
            pass


        self.cnxn.commit()
      
        
        logger.warning('the data is loaded')


    def from_sql_to_pandas(self, chunksize:int, id_value:str) -> pd.DataFrame:
        """Fetch data from the database to a Pandas DataFrame.

        :param chunksize: The number of rows to fetch in each iteration.
        :type chunksize: int
        :param id_value: The column used for ordering and pagination.
        :type id_value: str
        :param chunksize:int: 
        :param id_value:str: 
        :returns: The concatenated DataFrame containing all fetched data.
        :rtype: pd.DataFrame

        """
        
        offset=0
        dfs=[]
       
        
        while True:
            query=f"""
            SELECT * FROM {self.table_name}
                ORDER BY {id_value}
                OFFSET  {offset}  ROWS
                FETCH NEXT {chunksize} ROWS ONLY  
            """
            data = pd.read_sql_query(query,self.cnxn) 
            logger.info(f'the shape of the chunk: {data.shape}')
            dfs.append(data)
            offset += chunksize
            if len(dfs[-1]) < chunksize:
                logger.warning('loading the data from SQL is finished')
                logger.debug('connection is closed')
                break
        df = pd.concat(dfs)

        return df

    def update_table(self, condition: str, new_data: pd.Series) -> None:
        """Update rows in the database table based on a specified condition.

        :param condition: The condition to identify which rows to update (e.g., "column_name = value").
        :type condition: str
        :param new_data: The data to be updated as a Pandas Series.
        :type new_data: pd.Series
        :param condition: str: 
        :param new_data: pd.Series: 

        """
        # Check if the data Series contains the required columns
        if not set(new_data.index).issubset(self.get_table_columns()):
            logger.error("Data contains columns not present in the database table.")
            return

        # Ensure all values are non-null
        new_data = new_data.fillna(None)

        # Prepare a tuple for insertion
        values = tuple(new_data[column.lower()] for column in self.get_table_columns())

        # Define the SQL query for updating rows based on the condition
        query = f"UPDATE {self.table_name} SET {', '.join(f'{col} = ?' for col in self.get_table_columns())} WHERE {condition}"

        # Execute the query
        cursor = self.cnxn.cursor()
        cursor.execute(query, values)
        self.cnxn.commit()
        cursor.close()

   