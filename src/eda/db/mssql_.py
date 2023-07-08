"""
Connector class to connect to MS SQL Server
"""
import sqlalchemy
import pyodbc
import urllib
import pandas as pd
from sqlalchemy import event

class SQLClient:
    """
    Establishes a connection to MS SQL Server
    """

    def __init__(self, server=None, db=None, user=None, password=None, connection_string=None):

        # default odbc format:
        odbc_string = 'DRIVER={driver};SERVER={server};DATABASE={db};UID={user_id};PWD={password};ansi=True'

        # Some checks. Either connection string or details must be given
        if connection_string is None:
            if server is None:
                assert False, "Server name must be provided"
            if db is None:
                assert False, "DB name must be provided"
            if user is None:
                assert False, "User id must be provided"
            if password is None:
                assert False, "Password must be provided"
            connection_string = odbc_string.format(
                # driver='{SQL Server}',
                driver='{ODBC Driver 17 for SQL Server}',
                server=server,
                db=db,
                user_id=user,
                password=password)
        #print(connection_string)
        # logger.info("Connecting to db...")
        #try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        self.cursor = cursor

        self._engine = self.get_engine(server, db, user, password, connection_string)
        # self._engine = sqlalchemy.create_engine(
        #    "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(connection_string))
        #except:
        # logger.info("Db connection established successfully.")
    @property
    def engine(self):
        return self._engine

    def get_engine(self, server=None, db=None, user=None, password=None, connection_string=None):
        """
        Gets sqlalchemy engine
        :param password:
        :return:
        """
        # default odbc format:
        odbc_string = 'DRIVER={driver};SERVER={server};DATABASE={db};UID={user_id};PWD={password};ansi=True'

        # Some checks. Either connection string or details must be given
        if connection_string is None:
            if server is None:
                assert False, "Server name must be provided"
            if db is None:
                assert False, "DB name must be provided"
            if user is None:
                assert False, "User id must be provided"
            if password is None:
                assert False, "Password must be provided"

            connection_string = odbc_string.format(
                driver='{SQL Server}',
                server=server,
                db=db,
                user_id=user,
                password=password)

        self._engine = sqlalchemy.create_engine(
            "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(connection_string)) # , fast_executemany = True
        # , fast_executemany = True is throwing error. REVISIT.
        # # Added on 5/8/2021 to improve the performance. https://github.com/pandas-dev/pandas/issues/15276
        # NOTE: it is no longer necessary to define the below function. fast_executemany takes care of it.
        # @event.listens_for(self._engine, 'before_cursor_execute')
        # def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        #     if executemany:
        #         cursor.fast_executemany = True
        #         cursor.commit()

        return self._engine

    def close(self):
        """
        Closes the connection
        :return:
        """
        self._engine.dispose()

    def load_data(self, sql):
        """
        Loads the data by using the connection and calling the sql statement
        :param conn:
        :param sql:
        :return:
        """
        try:
            input_df = pd.read_sql(sql=sql, con=self._engine)
        except Exception as error:
            # logger.exception("Error while fetching the data. Error: " + str(error))
            input_df = None
        finally:
            self._engine.close()
        return input_df
