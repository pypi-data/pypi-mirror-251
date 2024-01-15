#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine, inspect
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import numpy as np 
import fastcore.basics as fcb
from jobbot_algos.core import logger


# In[2]:


class PostgresConnector:
    def __init__(
        self, 
        ssh_host, 
        ssh_username, 
        ssh_password, 
        local_host, 
        postgres_username, 
        postgres_password, 
        database,
    ):
        self.ssh_host = ssh_host
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.local_host = local_host
        self.postgres_username = postgres_username
        self.postgres_password = postgres_password
        self.database = database
        
        self.server = SSHTunnelForwarder(
            (ssh_host, 22), 
            ssh_username=ssh_username, 
            ssh_password=ssh_password, 
            remote_bind_address=(local_host, 5432),
            local_bind_address=('127.0.0.1', 0),
        )
        
        logger.info(f"SUCCESS: initialized PostgresConnector")
        
    def create_engine(self):
        server = self.server
        local_port = str(server.local_bind_port)
        engine = create_engine(f'postgresql://{self.postgres_username}:{self.postgres_password}@{self.local_host}:{local_port}/{self.database}')
        return engine


# In[3]:


# SET UP YOUR CREDS:
postgres_creds = {'ssh_host':'185.247.17.122',
                  'ssh_username':'root',
                  'ssh_password':'aRGgMeM7wBQ2m*',
                  'local_host':'localhost',
                  'postgres_username':'jobbot',
                  'postgres_password':'12345',
                  'database':'jobbot_db'
                 }


# # 1. Method for executing a command:

# In[4]:


@fcb.patch_to(PostgresConnector)
def execute(self, sql_command):
    
    server = self.server
    
    server.start()
    engine = self.create_engine()
    engine.execute(sql_command)
    server.stop()
    
    logger.info(f"Executed command: {sql_command} in database: {self.database}")


# In[5]:


# EXAMPLE:
# pc.execute('some command')


# # 2. Method for creating schema:

# In[6]:


@fcb.patch_to(PostgresConnector)
def create_schema(self, schema_name):
    self.execute(f'CREATE SCHEMA {schema_name};')
    logger.info(f"SUCCESS: schema {schema_name} was created in database: {self.database}")


# In[7]:


# EXAMPLE:
# pc.create_schema('test_schema')


# # 3. Method for dropping schema:

# In[8]:


@fcb.patch_to(PostgresConnector)
def drop_schema(self, schema_name):
    self.execute(f'DROP SCHEMA {schema_name} CASCADE;')
    logger.info(f"SUCCESS: schema {schema_name} was dropped from database: {self.database}")


# In[9]:


# EXAMPLE:
# pc.drop_schema('test_schema')


# # 4. Method for checking connections to database: 

# In[10]:


@fcb.patch_to(PostgresConnector)
def check_connection(self):
    try:
        server = self.server
        server.start()
        engine = self.create_engine()
        n = pd.read_sql("SELECT COUNT(*) FROM pg_catalog.pg_type", engine).values[0][0]
        server.stop()
        assert (n > 100), f"pg_catalog.pg_type should have > 400 rows, got {n} instead"
        logger.info("Connection to database established")
    except Exception as e:
        logger.error(f"Connection to database has failed")
        raise e


# In[11]:


# EXAMPLE:
# pc = PostgresConnector(**postgres_creds)
# pc.check_connection()


# # 5. Method for creating table:

# In[12]:


@fcb.patch_to(PostgresConnector)
def create_table(self,
    df,
    table_name: str,
    schema: str = "public",
):
    
    ## Run some checks:
    # column "inserted_into_db_msk" will be created automatically, it shouldn't be passed:
    if ("inserted_into_db_msk" in df.columns):  #
        raise NotImplementedError("Did not expect 'inserted_into_db_msk' column in df")
    
    # check that table name starts not from numeric:
    if not table_name[0].isalpha():  
        raise Exception(f"Table name shouldn't start from numeric value. Passed table name: {table_name}")
        
        
    # numpy to Postgres type map
    np_to_postgres_type = {
        np.dtype("int64"): "bigint",
        np.dtype("float32"): "real",
        np.dtype("float64"): "real",
        np.dtype("O"): "text",
        np.dtype("datetime64[ns]"): "timestamp",
        np.dtype("bool"): "boolean"}
    
    # part of query for defining columns names and types, according to the types in initial df:
    sql_columns_list = []

    for column, col_type in zip(df.columns, df.dtypes):
        sql_columns_list.append(f"{column} {np_to_postgres_type[col_type]}")

    # creating final command
    sql_column_creation_command = ", ".join(sql_columns_list)
        
    final_sql_command = f"""
                         CREATE TABLE {schema}.{table_name}
                         ({sql_column_creation_command},
                         inserted_into_db_msk timestamp DEFAULT (current_timestamp AT TIME ZONE 'Europe/Moscow'));
                         """
    
    # Finally creating that command
    server = self.server
    server.start()
    engine = self.create_engine()
    engine.execute(final_sql_command)
    server.stop()
    
    logger.info(f"Table named {table_name} was created")


# In[13]:


# EXAMPLE:
# pc = PostgresConnector(**postgres_creds)
# df = pd.DataFrame({'col1':[1,2,3], 'col2':[111,2212,3123131]})
# pc.create_table(df=df, table_name='test2', schema='test_schema')


# # 6. Method for downloading data:

# In[14]:


@fcb.patch_to(PostgresConnector)
def download(self, sql_query: str):

    server = self.server
    server.start()
    engine = self.create_engine()
    result = pd.read_sql_query(sql=sql_query, con=engine)
    server.stop()
    return result


# In[15]:


# EXAMPLE:
# pc.download("SELECT * FROM pg_catalog.pg_type")


# # 7. Method for checking if table exists:

# In[16]:


@fcb.patch_to(PostgresConnector)
def table_exists(self, table_name: str, schema: str):
    try:
        sql_query_to_check_existence = f"SELECT * FROM {schema}.{table_name} LIMIT 1"
        self.download(sql_query=sql_query_to_check_existence)
        return True
    except:
        return False


# In[17]:


# EXAMPLE:
# pc.table_exists(table_name='test', schema='test_schema')


# # 8. Method for deleting a table:

# In[18]:


@fcb.patch_to(PostgresConnector)
def delete_table(
    self,
    table_name: str,
    schema: str,
):
    if not self.table_exists(table_name=table_name, schema=schema):
        raise Exception(
            f"Trying to delete non-existent table. Table {schema}.{table_name} doesn't exist"
        )

        
    server = self.server
    server.start()
    engine = self.create_engine()
        
    engine.execute(f"DROP TABLE IF EXISTS {schema}.{table_name};")
    server.stop()
    logger.info(f"Table named {table_name} was deleted")


# In[19]:


# EXAMPLE:
# pc.delete_table(table_name='test2', schema='test_schema')


# # 9. Method for saving data into table:

# In[20]:


@fcb.patch_to(PostgresConnector)
def save(
    self,
    df: pd.DataFrame,
    table_name: str,
    schema: str,
    if_table_exists: str = "append",
):
    # check if correct parameters are inserted:
    if df.empty:
        raise Exception("The dataframe is empty")
    if if_table_exists not in ["append", "replace"]:
        raise ValueError(f"'{if_table_exists}' is not valid for if_table_exists")
    
    # if table doesn't exist - create it:
    if not self.table_exists(table_name=table_name, schema=schema):
        logger.info(f"The table named {table_name} doesn't exist. It will be created")
        self.create_table(df=df, table_name=table_name, schema=schema) 
    
    if if_table_exists == "replace":  
        logger.info("An existing table will be dropped and filled with fresh values")
        self.delete_table(table_name=table_name, schema=schema)
        self.save(df=df, table_name=table_name, schema=schema, if_table_exists="append")
        
    if if_table_exists == "append":  
        logger.info(f"Filling table {table_name} with values")  
        server = self.server
        server.start()
        engine = self.create_engine()
        df.to_sql(name=table_name, con=engine, schema=schema, index=False, if_exists="append")
        server.stop()


# In[21]:


# EXAMPLE:
# df = pd.DataFrame({'city':['Moscow','London','New York'], 'number':[10**2,20**2,30**2]})
# pc.save(df=df, table_name='test', schema='test_schema', if_table_exists='replace')


# # 10. Method for showing list of schemas:

# In[22]:


@fcb.patch_to(PostgresConnector)
def get_schemas_list(self):
    return self.download('SELECT nspname FROM pg_namespace').rename(columns={'nspname':'schema'})


# In[23]:


# EXAMPLE:
# pc.get_schemas_list()


# In[25]:


# # get creds:
# import os
# postgres_user = os.environ.get("POSTGRES_USER")
# postgres_pass = os.environ.get("POSTGRES_PASS")

# # test connection:
# pc = PostgresConnector(**postgres_creds)
# pc.check_connection()

# # test getting schema list:
# pc.get_schemas_list()

# # test schema creation:
# pc.create_schema('test_schema')

# # test create table:
# df = pd.DataFrame({'col1':[1,2,3], 'col2':[111,222,333]})
# pc.create_table(df=df, table_name='test', schema='test_schema')

# # test download
# assert len(pc.download("SELECT * FROM pg_catalog.pg_type")) != 0

# # test if table exists:
# assert pc.table_exists(table_name='test', schema='test_schema')


# # test save to table:
# df = pd.DataFrame({'col1':[1000,2000,3000], 'col2':[10**5,20**5,30**5]})
# pc.save(df=df, table_name='test', schema='test_schema', if_table_exists='append')

# df = pd.DataFrame({'city':['Moscow','London','New York'], 'number':[10**2,20**2,30**2]})
# pc.save(df=df, table_name='test', schema='test_schema', if_table_exists='replace')

# # test delete table:
# pc.delete_table(table_name='test', schema='test_schema')

# # test delete schema:
# pc.drop_schema('test_schema')

