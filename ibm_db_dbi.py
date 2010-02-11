# +--------------------------------------------------------------------------+
# |  Licensed Materials - Property of IBM                                    |
# |                                                                          |
# | (C) Copyright IBM Corporation 2007-2009                                  |
# +--------------------------------------------------------------------------+
# | This module complies with SQLAlchemy 0.4 and is                          |
# | Licensed under the Apache License, Version 2.0 (the "License");          |
# | you may not use this file except in compliance with the License.         |
# | You may obtain a copy of the License at                                  |
# | http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable |
# | law or agreed to in writing, software distributed under the License is   |
# | distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY |
# | KIND, either express or implied. See the License for the specific        |
# | language governing permissions and limitations under the License.        |
# +--------------------------------------------------------------------------+
# | Authors: Swetha Patel, Abhigyan Agrawal, Tarun Pasrija, Rahul Priyadarshi|
# | Version: 1.0                                                             |
# +--------------------------------------------------------------------------+

"""
This module implements the Python DB API Specification v2.0 for DB2 database.
"""

import types, string, time, datetime, decimal, exceptions
from sets import ImmutableSet
import ibm_db

import logging
logging.basicConfig()
logger = logging.getLogger('  >  ibm_db_dbi  >  ')
logger.setLevel(logging.INFO)  # use logging.DEBUG in order to enable debug trace

# Constants for specifying database connection options.
SQL_ATTR_AUTOCOMMIT = ibm_db.SQL_ATTR_AUTOCOMMIT
SQL_ATTR_CURRENT_SCHEMA = ibm_db.SQL_ATTR_CURRENT_SCHEMA
SQL_AUTOCOMMIT_OFF = ibm_db.SQL_AUTOCOMMIT_OFF
SQL_AUTOCOMMIT_ON = ibm_db.SQL_AUTOCOMMIT_ON
ATTR_CASE = ibm_db.ATTR_CASE
CASE_NATURAL = ibm_db.CASE_NATURAL
CASE_LOWER = ibm_db.CASE_LOWER
CASE_UPPER = ibm_db.CASE_UPPER
SQL_FALSE = ibm_db.SQL_FALSE
SQL_TRUE = ibm_db.SQL_TRUE
SQL_TABLE_STAT = ibm_db.SQL_TABLE_STAT
SQL_INDEX_CLUSTERED = ibm_db.SQL_INDEX_CLUSTERED
SQL_INDEX_OTHER = ibm_db.SQL_INDEX_OTHER
SQL_DBMS_VER = ibm_db.SQL_DBMS_VER
SQL_DBMS_NAME = ibm_db.SQL_DBMS_NAME

# Module globals
apilevel = '2.0'
threadsafety = 0
paramstyle = 'qmark'
rowcount_prefetch = False


class Error(exceptions.StandardError):
    """This is the base class of all other exception thrown by this
    module.  It can be use to catch all exceptions with a single except
    statement.
    
    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        super(Error, self).__init__(message)
        self.message = message
    def __str__(self):
        """Converts the message to a string."""
        return 'ibm_db_dbi::'+str(self.__class__.__name__)+': '+str(self.message)


class Warning(exceptions.StandardError):
    """This exception is used to inform the user about important 
    warnings such as data truncations.

    """
    def __init__(self, message):
        """This is the constructor which take one string argument."""
        super(Warning, self).__init__(message)
        self.message = message
    def __str__(self):
        """Converts the message to a string."""
        return 'ibm_db_dbi::'+str(self.__class__.__name__)+': '+str(self.message)


class InterfaceError(Error):
    """This exception is raised when the module interface is being
    used incorrectly.

    """
    pass


class DatabaseError(Error):
    """This exception is raised for errors related to database."""
    pass


class InternalError(DatabaseError):
    """This exception is raised when internal database error occurs,
    such as cursor is not valid anymore.

    """
    pass


class OperationalError(DatabaseError):
    """This exception is raised when database operation errors that are
    not under the programmer control occur, such as unexpected
    disconnect.

    """ 
    pass


class ProgrammingError(DatabaseError):
    """This exception is raised for programming errors, such as table 
    not found.

    """
    pass

class IntegrityError(DatabaseError):
    """This exception is thrown when errors occur when the relational
    integrity of database fails, such as foreign key check fails. 

    """
    pass


class  DataError(DatabaseError):
    """This exception is raised when errors due to data processing,
    occur, such as divide by zero. 

    """
    pass


class NotSupportedError(DatabaseError):
    """This exception is thrown when a method in this module or an 
    database API is not supported.

    """
    pass


def Date(year, month, day):
    """This method can be used to get date object from integers, for 
    inserting it into a DATE column in the database.

    """
    return datetime.date(year, month, day)

def Time(hour, minute, second):
    """This method can be used to get time object from integers, for 
    inserting it into a TIME column in the database.

    """
    return datetime.time(hour, minute, second)

def Timestamp(year, month, day, hour, minute, second):
    """This method can be used to get timestamp object from integers, 
    for inserting it into a TIMESTAMP column in the database.

    """
    return datetime.datetime(year, month, day, hour, minute, second)

def DateFromTicks(ticks):
    """This method can be used to get date object from ticks seconds,
    for inserting it into a DATE column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.date(time_tuple[0], time_tuple[1], time_tuple[2])

def TimeFromTicks(ticks):
    """This method can be used to get time object from ticks seconds,
    for inserting it into a TIME column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.time(time_tuple[3], time_tuple[4], time_tuple[5])

def TimestampFromTicks(ticks):
    """This method can be used to get timestamp object from ticks  
    seconds, for inserting it into a TIMESTAMP column in the database.

    """
    time_tuple = time.localtime(ticks)
    return datetime.datetime(time_tuple[0], time_tuple[1], time_tuple[2], 
                                time_tuple[3], time_tuple[4], time_tuple[5])

def Binary(string):
    """This method can be used to store binary information, for 
    inserting it into a binary type column in the database.

    """
    if not isinstance( string, types.StringType):
        raise InterfaceError("Binary function expects type string argument.")
    return buffer(string)


class DBAPITypeObject(ImmutableSet):
    """Class used for creating objects that can be used to compare
    in order to determine the python type to provide in parameter 
    sequence argument of the execute method.

    """
    def __init__(self, col_types):
        """Constructor for DBAPITypeObject.  It takes a tuple of 
        database column type as an argument.
        """
        super(DBAPITypeObject, self).__init__(col_types)
        self.col_types = col_types

    def __cmp__(self, cmp):
        """This method checks if the string compared with is in the 
        tuple provided to the constructor of this object.  It takes 
        string as an argument. 
 
        """
        if cmp in self.col_types:
            return 0
        if cmp < self.col_types:
            return 1
        else:
            return -1

# The user can use these objects to compare the database column types
# with in order to determine the python type to provide in the 
# parameter sequence argument of the execute method.
STRING = DBAPITypeObject(("CHARACTER", "CHAR", "VARCHAR", 
                          "CHARACTER VARYING", "CHAR VARYING", "STRING",))

TEXT = DBAPITypeObject(("CLOB", "CHARACTER LARGE OBJECT", "CHAR LARGE OBJECT",  "XML",))

BINARY = DBAPITypeObject(("BLOB", "BINARY LARGE OBJECT",))

NUMBER = DBAPITypeObject(("INTEGER", "INT", "SMALLINT", "BIGINT",))

FLOAT = DBAPITypeObject(("FLOAT", "REAL", "DOUBLE", "DECFLOAT"))

DECIMAL = DBAPITypeObject(("DECIMAL", "DEC", "NUMERIC", "NUM",))

DATE = DBAPITypeObject(("DATE",))

TIME = DBAPITypeObject(("TIME",))

DATETIME = DBAPITypeObject(("TIMESTAMP",))

ROWID = DBAPITypeObject(())

# This method is used to determine the type of error that was 
# generated.  It takes an exception instance as an argument, and 
# returns exception object of the appropriate type.
def _get_exception(inst):
    # These tuple are used to determine the type of exceptions that are
    # thrown by the database.  They store the SQLSTATE code and the
    # SQLSTATE class code(the 2 digit prefix of the SQLSTATE code)  
    warning_error_tuple=('01', )
    data_error_tuple=('02', '22', '10601', '10603', '10605', '10901', '10902', 
                                                               '38552', '54')

    operational_error_tuple = ( '08', '09', '10502', '10000', '10611', '38501', 
                          '38503', '38553', '38H01', '38H02', '38H03', '38H04',
                                   '38H05', '38H06', '38H07', '38H09', '38H0A')

    integrity_error_tuple = ('23', )

    internal_error_tuple = ('24', '25', '26', '2D', '51', '57')

    programming_error_tuple = ('08002', '07', 'OD', 'OF','OK','ON','10', '27',
                               '28', '2E', '34', '36', '38', '39', '56', '42',
                               '3B', '40', '44', '53', '55', '58', '5U', '21')

    not_supported_error_tuple = ('0A', '10509')

    # These tuple are used to determine the type of exceptions that are
    # thrown from the driver module. 
    interface_exceptions = (                  "Supplied parameter is invalid",
                                        "ATTR_CASE attribute must be one of "
                                    "CASE_LOWER, CASE_UPPER, or CASE_NATURAL",
                          "Connection or statement handle must be passed in.",
                                                       "Param is not a tuple")

    programming_exceptions = (                     "Connection is not active", 
                                                 "qualifier must be a string",
                                                   "unique must be a boolean",
                                                       "Parameters not bound",
                                                     "owner must be a string",
                                                "table_name must be a string",
                                                "table type must be a string", 
                                               "column_name must be a string", 
                                                "Column ordinal out of range", 
                                            "procedure name must be a string",
                              "Requested row number must be a positive value", 
                                     "Options Array must have string indexes")

    database_exceptions = (                                   "Binding Error", 
                                   "Column information cannot be retrieved: ", 
                                            "Column binding cannot be done: ",
                                             "Failed to Determine XML Size: ")

    statement_exceptions = (                     "Statement Execute Failed: ",
                                                    "Describe Param Failed: ",
                                                      "Sending data failed: ",
                                                            "Fetch Failure: ",
                                                  "SQLNumResultCols failed: ",
                                                       "SQLRowCount failed: ",
                                                   "SQLGetDiagField failed: ",
                                                 "Statement prepare Failed: ")

    operational_exceptions = (          "Connection Resource cannot be found", 
                                                  "Failed to Allocate Memory",
                                                    "Describe Param Failed: ",
                                                 "Statement Execute Failed: ",
                                                      "Sending data failed: ", 
                                     "Failed to Allocate Memory for XML Data",
                                     "Failed to Allocate Memory for LOB Data")

    # First check if the exception is from the database.  If it is 
    # determine the SQLSTATE code which is used further to determine 
    # the exception type.  If not check if the exception is thrown by 
    # by the driver and return the appropriate exception type.  If it 
    # is not possible to determine the type of exception generated 
    # return the generic Error exception.
    if inst is not None:
        message = repr(inst)
        if message.startswith("Exception('") and message.endswith("',)"):
            message = message[11:]
            message = message[:len(message)-3]

        index = message.find('SQLSTATE=')
        if( message != '') & (index != -1):
            error_code = message[(index+9):(index+14)]
            prefix_code = error_code[:2]
        else:
            for key in interface_exceptions:
                if message.find(key) != -1:
                    return InterfaceError(message)
            for key in programming_exceptions:
                if message.find(key) != -1:
                    return ProgrammingError(message)
            for key in operational_exceptions:
                if message.find(key) != -1:
                    return OperationalError(message)
            for key in database_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)  
            for key in statement_exceptions:
                if message.find(key) != -1:
                    return DatabaseError(message)
            return Error(message)
    else:
        return Error('An error has occured')

    # First check if the SQLSTATE is in the tuples, if not check
    # if the SQLSTATE class code is in the tuples to determine the
    # exception type. 
    if ( error_code in warning_error_tuple or 
         prefix_code in warning_error_tuple ):
        return Warning(message)
    if ( error_code in data_error_tuple or 
         prefix_code in data_error_tuple ):
        return DataError(message)
    if ( error_code in operational_error_tuple or 
         prefix_code in operational_error_tuple ):
        return OperationalError(message)
    if ( error_code in integrity_error_tuple or 
         prefix_code in integrity_error_tuple ):
        return IntegrityError(message)
    if ( error_code in internal_error_tuple or
         prefix_code in internal_error_tuple ):
        return InternalError(message)
    if ( error_code in programming_error_tuple or
         prefix_code in programming_error_tuple ):
        return ProgrammingError(message)
    if ( error_code in not_supported_error_tuple or
         prefix_code in not_supported_error_tuple ):
        return NotSupportedError(message)
    return DatabaseError(message)

def connect(dsn,user='',password='',host='',database='',conn_options=None):
    """This method creates a connection to the database. It returns
        a ibm_db_dbi.Connection object.
    """
    logger.debug('connect: '+ repr(dsn))
    
    if dsn is None:
        raise InterfaceError("connect expects a not None dsn value") 
    
    if ((not isinstance(dsn, types.StringType)) and \
       (not isinstance(dsn, types.UnicodeType))) | \
       ((not isinstance(user, types.StringType)) and \
       (not isinstance(user, types.UnicodeType))) | \
       ((not isinstance(password, types.StringType)) and \
       (not isinstance(password, types.UnicodeType))) | \
       ((not isinstance(host, types.StringType)) and \
       (not isinstance(host, types.UnicodeType))) | \
       ((not isinstance(database, types.StringType)) and \
       (not isinstance(database, types.UnicodeType))):
        raise InterfaceError("connect expects the first five arguments to"
                                                      " be of type string or unicode")
    if conn_options is not None:
        if not isinstance(conn_options, dict):
            raise InterfaceError("connect expects the sixth argument"
                                 " (conn_options) to be of type dict")
        if not SQL_ATTR_AUTOCOMMIT in conn_options:
            conn_options[SQL_ATTR_AUTOCOMMIT] = SQL_AUTOCOMMIT_OFF
    else:
        conn_options = {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_ON}

    # If the dsn does not contain port and protocal adding database
    # and hostname is no good.  Add these when required, that is,
    # if there is a '=' in the dsn.  Else the dsn string is taken to be
    # a DSN entry.
    if dsn.find('=') != -1:
        if dsn[len(dsn) - 1] != ';':
            dsn = dsn + ";"
        if database != '' and dsn.find('DATABASE=') == -1:
            dsn = dsn + "DATABASE=" + database + ";"
        if host != '' and dsn.find('HOSTNAME=') == -1:
            dsn = dsn + "HOSTNAME=" + host + ";"
    else:
        dsn = "DSN=" + dsn + ";"

    if user != '' and dsn.find('UID=') == -1:
        dsn = dsn + "UID=" + user + ";"
    if password != '' and dsn.find('PWD=') == -1:
        dsn = dsn + "PWD=" + password + ";"
    try:    
        conn = ibm_db.connect(dsn, '', '', conn_options) 
        rowcount_prefetch = ibm_db.check_function_support(conn,ibm_db.SQL_API_SQLROWCOUNT)
        ibm_db.set_option(conn, {SQL_ATTR_CURRENT_SCHEMA : user}, 1)
    except Exception, inst:
        raise _get_exception(inst)

    return Connection(conn)

class Connection(object):
    """This class object represents a connection between the database 
    and the application.

    """
    def __init__(self, conn_handler):
        """Constructor for Connection object. It takes ibm_db 
        connection handler as an argument. 

        """
        self.conn_handler = conn_handler

        # Used to identify close cursors for generating exceptions 
        # after the connection is closed.
        self._cursor_list = []
        self.__dbms_name = ibm_db.get_db_info(conn_handler, SQL_DBMS_NAME)
        self.__dbms_ver = ibm_db.get_db_info(conn_handler, SQL_DBMS_VER)

    # This method is used to get the DBMS_NAME 
    def __get_dbms_name( self ):
        return self.__dbms_name

    # This attribute specifies the DBMS_NAME
    # It is a read only attribute. 
    dbms_name = property(__get_dbms_name, None, None, "")

    # This method is used to get the DBMS_ver 
    def __get_dbms_ver( self ):
        return self.__dbms_ver

    # This attribute specifies the DBMS_ver
    # It is a read only attribute. 
    dbms_ver = property(__get_dbms_ver, None, None, "")

    def close(self):
        """This method closes the Database connection associated with
        the Connection object.  It takes no arguments.

        """
        self.rollback()
        try:
            if self.conn_handler is None:
                raise ProgrammingError("Connection cannot be closed; "
                                     "connection is no longer active.")
            else:
                return_value = ibm_db.close(self.conn_handler)
        except Exception, inst:
            raise _get_exception(inst)
        self.conn_handler = None
        for index in range(len(self._cursor_list)):
            self._cursor_list[index].conn_handler = None
            self._cursor_list[index].stmt_handler = None
            self._cursor_list[index]._all_stmt_handlers = None
        return return_value

    def commit(self):
        """This method commits the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = ibm_db.commit(self.conn_handler)
        except Exception, inst:
            raise _get_exception(inst)
        return return_value

    def rollback(self):
        """This method rollbacks the transaction associated with the
        Connection object.  It takes no arguments.

        """
        try:
            return_value = ibm_db.rollback(self.conn_handler)
        except Exception, inst:
            raise _get_exception(inst)
        return return_value

    def cursor(self):
        """This method returns a Cursor object associated with the 
        Connection.  It takes no arguments.

        """
        if self.conn_handler is None:
            raise ProgrammingError("Cursor cannot be returned; "
                               "connection is no longer active.")
        cursor = Cursor(self.conn_handler, self)
        self._cursor_list.append(cursor)
        return cursor

    # Sets connection attribute values
    def set_option(self, attr_dict):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        return ibm_db.set_option(self.conn_handler, attr_dict, 1)

    # Retrieves connection attributes values
    def get_option(self, attr_key):
        """Input: connection attribute key
           Return: current setting of the resource attribute requested
        """
        return ibm_db.get_option(self.conn_handler, attr_key, 1)

    # Sets connection AUTOCOMMIT attribute
    def set_autocommit(self, is_on):
        """Input: connection attribute: true if AUTOCOMMIT ON, false otherwise (i.e. OFF)
           Return: True on success or False on failure
        """
        try:
          if is_on:
            is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_ON}, 1)
          else:
            is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_AUTOCOMMIT : SQL_AUTOCOMMIT_OFF}, 1)
        except Exception, inst:
          raise _get_exception(inst)
        return is_set

    # Sets connection attribute values
    def set_current_schema(self, schema_name):
        """Input: connection attribute dictionary
           Return: True on success or False on failure
        """
        self.current_schema = schema_name
        try:
          is_set = ibm_db.set_option(self.conn_handler, {SQL_ATTR_CURRENT_SCHEMA : schema_name}, 1)
        except Exception, inst:
          raise _get_exception(inst)
        return is_set

    # Retrieves connection attributes values
    def get_current_schema(self):
        """Return: current setting of the schema attribute
        """
        try:
          conn_schema = ibm_db.get_option(self.conn_handler, SQL_ATTR_CURRENT_SCHEMA, 1)
          if conn_schema is not None and conn_schema != '':
            self.current_schema = conn_schema
        except Exception, inst:
          raise _get_exception(inst)
        return self.current_schema

    # Retrieves the IBM Data Server version for a given Connection object
    def server_info(self):
        """Return: tuple (DBMS_NAME, DBMS_VER)
        """
        try:
          server_info = []
          server_info.append(self.dbms_name)
          server_info.append(self.dbms_ver)
        except Exception, inst:
          raise _get_exception(inst)
        return tuple(server_info)
    
    def set_case(self, server_type, str_value):
        return str_value.upper()

    # Retrieves the tables for a specified schema (and/or given table name)
    def tables(self, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of table metadata dicts for the specified schema
        """
        logger.debug('tables( ' + repr(schema_name) + ', ' + repr(table_name) + ' )')
            
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:      
          stmt = ibm_db.tables(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception, inst:
          raise _get_exception(inst)

        logger.debug('tables: '+repr(result))
        return result

    # Retrieves metadata pertaining to index for specified schema (and/or table name)
    def indexes(self, unique = True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of index metadata dicts for the specified table
        Example:
           Index metadata retrieved from schema 'PYTHONIC.TEST_TABLE' table
           {
           'TABLE_SCHEM':       'PYTHONIC',              'TABLE_CAT':          None, 
           'TABLE_NAME':        'ENGINE_USERS',          'PAGES':              None, 
           'COLUMN_NAME':       'USER_ID'                'FILTER_CONDITION':   None, 
           'INDEX_NAME':        'SQL071201150750170',    'CARDINALITY':        None,
           'ORDINAL_POSITION':   1,                      'INDEX_QUALIFIER':   'SYSIBM', 
           'TYPE':               3, 
           'NON_UNIQUE':         0, 
           'ASC_OR_DESC':       'A'
           }
        """
        logger.debug('indexes( '+str(unique)+', '+repr(schema_name)+', '+repr(table_name)+' )')
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.statistics(self.conn_handler, None, schema_name, table_name, unique)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              if row['TYPE'] == SQL_INDEX_OTHER:
                  result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception, inst:
          raise _get_exception(inst)

        logger.debug('indexes: '+str(result))
        return result        

    # Retrieves metadata pertaining to primary keys for specified schema (and/or table name)
    def primary_keys(self, unique = True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of PK metadata dicts for the specified table
        Example:
           PK metadata retrieved from 'PYTHONIC.ORDERS' table
           {  
           'TABLE_SCHEM':  'PYTHONIC',                 'TABLE_CAT': None, 
           'TABLE_NAME':   'ORDERS', 
           'COLUMN_NAME':  'ORDER_ID'
           'PK_NAME':      'SQL071128122038680', 
           'KEY_SEQ':       1
           }
        """
        logger.debug('primary_keys( '+str(unique)+', '+ repr(schema_name) +', '+repr(table_name)+' )')
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.primary_keys(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception, inst:
          raise _get_exception(inst)

        logger.debug('primary_keys: '+repr(result))
        return result        

    # Retrieves metadata pertaining to foreign keys for specified schema (and/or table name)
    def foreign_keys(self, unique = True, schema_name=None, table_name=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of FK metadata dicts for the specified table
        Example:
           FK metadata retrieved from 'PYTHONIC.ENGINE_EMAIL_ADDRESSES' table
           {  
           'PKTABLE_SCHEM': 'PYTHONIC',                 'PKTABLE_CAT':    None, 
           'PKTABLE_NAME':  'ENGINE_USERS',             'FKTABLE_CAT':    None,
           'PKCOLUMN_NAME': 'USER_ID',                  'UPDATE_RULE':    3,
           'PK_NAME':       'SQL071205090958680',       'DELETE_RULE':    3
           'KEY_SEQ':        1,                         'DEFERRABILITY':  7, 
           'FK_NAME':       'SQL071205091000160', 
           'FKCOLUMN_NAME': 'REMOTE_USER_ID', 
           'FKTABLE_NAME':  'ENGINE_EMAIL_ADDRESSES', 
           'FKTABLE_SCHEM': 'PYTHONIC' 
           }
        """
        logger.debug('foreign_keys( '+str(unique)+', '+repr(schema_name)+', '+repr(table_name)+' )')
        result = []
        if schema_name is not None:
            schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
            table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.foreign_keys(self.conn_handler, None, None, None, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
              result.append( row )
              i += 1    
              row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)
        except Exception, inst:
          raise _get_exception(inst)

        logger.debug('foreign_keys: '+repr(result))
        return result        
    
    # Retrieves the columns for a specified schema (and/or table name and column name)
    def columns(self, schema_name=None, table_name=None, column_names=None):
        """Input: connection - ibm_db.IBM_DBConnection object
           Return: sequence of column metadata dicts for the specified schema
        Example:
           Column metadata retrieved from schema 'PYTHONIC.FOO' table, column 'A'
           {
           'TABLE_NAME':        'FOO',        'NULLABLE':           1, 
           'ORDINAL_POSITION':   2L,          'REMARKS':            None, 
           'COLUMN_NAME':       'A',          'BUFFER_LENGTH':      30L, 
           'TYPE_NAME':         'VARCHAR',    'SQL_DATETIME_SUB':   None, 
           'COLUMN_DEF':         None,        'DATA_TYPE':          12, 
           'IS_NULLABLE':       'YES',        'SQL_DATA_TYPE':      12, 
           'COLUMN_SIZE':        30L,         'TABLE_CAT':          None, 
           'CHAR_OCTET_LENGTH':  30L,         'TABLE_SCHEM':       'PYTHONIC',
           'NUM_PREC_RADIX':     None,
           'DECIMAL_DIGITS':     None
           }
        """
        logger.debug('columns( '+repr(schema_name)+', '+repr(table_name)+', '+repr(column_names)+' )')
        result = []
        if schema_name is not None:
          schema_name = self.set_case("DB2_LUW", schema_name)
        if table_name is not None:
          table_name = self.set_case("DB2_LUW", table_name)

        try:
          stmt = ibm_db.columns(self.conn_handler, None, schema_name, table_name)
          row = ibm_db.fetch_assoc(stmt)
          i = 0
          while (row):
            result.append( row )
            i += 1    
            row = ibm_db.fetch_assoc(stmt)
          ibm_db.free_result(stmt)

          col_names_lower = []
          if column_names is not None:
            for name in column_names:
              col_names_lower.append(name.lower())
            include_columns = []
            if column_names and column_names != '':
              for column in result:
                if column['COLUMN_NAME'].lower() in col_names_lower:
                  column['COLUMN_NAME'] = column['COLUMN_NAME'].lower()
                  include_columns.append(column)
              result = include_columns
        except Exception, inst:
          raise _get_exception(inst)

        logger.debug('columns( '+repr(column_names)+': '+repr(result)+' )')
        return result


# Defines a cursor for the driver connection
class Cursor(object):
    """This class represents a cursor of the connection.  It can be
    used to process an SQL statement.
    """
    
    # This method is used to get the description attribute.
    def __get_description(self):
        """ If this method has already been called, after executing a select statement,
            return the stored information in the self.__description.
        """
        if self.__description is not None:
            return self.__description 

        self.__description = []
        if self.stmt_handler is None:
            return None
        try:
            num_columns = ibm_db.num_fields(self.stmt_handler)
            """ If the execute statement did not produce a result set return None.
            """
            if num_columns == False:
                return None
            for column_index in range(num_columns):
                column_desc = []
                column_desc.append(ibm_db.field_name(self.stmt_handler,
                                                          column_index))
                type = ibm_db.field_type(self.stmt_handler, column_index)
                type = type.upper()
                if STRING.__cmp__(type) == 0:
                    column_desc.append(STRING)
                if TEXT.__cmp__(type) == 0:
                    column_desc.append(TEXT)
                if BINARY.__cmp__(type) == 0:
                    column_desc.append(BINARY)
                if NUMBER.__cmp__(type) == 0:
                    column_desc.append(NUMBER) 
                if FLOAT.__cmp__(type) == 0:
                    column_desc.append(FLOAT)                
                if DECIMAL.__cmp__(type) == 0:
                    column_desc.append(DECIMAL)
                if DATE.__cmp__(type) == 0:
                    column_desc.append(DATE)
                if TIME.__cmp__(type) == 0:
                    column_desc.append(TIME)
                if DATETIME.__cmp__(type) == 0:
                    column_desc.append(DATETIME)
                if ROWID.__cmp__(type) == 0:
                    column_desc.append(ROWID)

                column_desc.append(ibm_db.field_display_size(
                                             self.stmt_handler, column_index))

                column_desc.append(ibm_db.field_display_size(
                                             self.stmt_handler, column_index))
                
                column_desc.append(ibm_db.field_precision(
                                             self.stmt_handler, column_index))

                column_desc.append(ibm_db.field_scale(self.stmt_handler,
                                                                column_index))

                column_desc.append(None)
                self.__description.append(column_desc)
        except Exception, inst:
            raise _get_exception(inst)

        return self.__description

    # This attribute provides the metadata information of the columns  
    # in the result set produced by the last execute function.  It is
    # a read only attribute.
    description = property(fget = __get_description)

    # This method is used to get the rowcount attribute. 
    def __get_rowcount( self ):
        return self.__rowcount

    # This attribute specifies the number of rows the last executeXXX()
    # produced or affected.  It is a read only attribute. 
    rowcount = property(__get_rowcount, None, None, "")
    
    # This method is used to get the Connection object
    def __get_connection( self ):
        return self.__connection
    
    # This attribute specifies the connection object.
    # It is a read only attribute. 
    connection = property(__get_connection, None, None, "")

    def __init__(self, conn_handler):
        """Constructor for Cursor object. It takes ibm_db connection 
        handler as an argument.

        """
        # This attribute is used to determine the fetch size for fetchmany
        # operation. It is a read/write attribute
        self.arraysize = 1
        self.__rowcount = -1
        self._result_set_produced = False
        self.__description = None
        self.conn_handler = conn_handler
        self.stmt_handler = None
        self._is_scrollable_cursor = False
    
    def __init__(self, conn_handler, conn_object):
        """Constructor for Cursor object. It takes ibm_db connection
        handler as an argument.
        """
        
        # This attribute is used to determine the fetch size for fetchmany
        # operation. It is a read/write attribute
        self.arraysize = 1
        self.__rowcount = -1
        self._result_set_produced = False
        self.__description = None
        self.conn_handler = conn_handler
        self.stmt_handler = None
        self._is_scrollable_cursor = False
        self.__connection = conn_object
    
    # This method closes the statemente associated with the cursor object.
    # It takes no argument.
    def close(self):
        """This method closes the cursor object.  After this method is 
        called the cursor object is no longer usable.  It takes no
        arguments.

        """
        if self.conn_handler is None:
            raise ProgrammingError("Cursor cannot be closed; "
                             "connection is no longer active.")
        try:
            return_value = ibm_db.free_stmt(self.stmt_handler)
        except Exception, inst:
            raise _get_exception(inst)
        self.stmt_handler = None
        self.conn_handler = None
        self._all_stmt_handlers = None
        return return_value

    # helper for calling procedure
    def _callproc_helper(self, procname, parameters=None):
        if parameters is not None:
            buff = []
            CONVERT_STR = (datetime.datetime, datetime.date, datetime.time, buffer)
            # Convert date/time and binary objects to string for 
            # inserting into the database. 
            for param in parameters:
                if isinstance(param, CONVERT_STR):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)
            
            try:
                result = ibm_db.callproc(self.conn_handler, procname,parameters)
            except Exception, inst:
                raise _get_exception(inst)
        else:
            try:
                result = ibm_db.callproc(self.conn_handler, procname)
            except Exception, inst:
                raise _get_exception(inst)
        return result
       

    def callproc(self, procname, parameters=None):
        """This method can be used to execute a stored procedure.  
        It takes the name of the stored procedure and the parameters to
        the stored procedure as arguments. 

        """
        if not isinstance(procname, types.StringType) and not isinstance(procname, types.UnicodeType):
            raise InterfaceError("callproc expects the first argument to " 
                                                       "be of type String or Unicode.")
        if parameters is not None:
            if not isinstance(parameters, (types.ListType, types.TupleType)):
                raise InterfaceError("callproc expects the second argument"
                                       " to be of type list or tuple.")
        result = self._callproc_helper(procname, parameters)
        return_value = None
        self.__description = None
        self._all_stmt_handlers = []
        if isinstance(result, types.TupleType):
            self.stmt_handler = result[0]
            return_value = result[1:]
        else:
            self.stmt_handler = result
        self._result_set_produced = True
        return return_value

    # Helper for preparing an SQL statement. 
    def _prepare_helper(self, operation, parameters=None):
        try:
            ibm_db.free_stmt(self.stmt_handler)
        except:
            pass

        try:
            self.stmt_handler = ibm_db.prepare(self.conn_handler, operation)
        except Exception, inst:
            raise _get_exception(inst)

    # Helper for preparing an SQL statement.
    def _set_cursor_helper(self):
        self._result_set_produced = False
        
        try:
            num_columns = ibm_db.num_fields(self.stmt_handler)
        except Exception, inst:
            raise _get_exception(inst)
        if not num_columns:
            return True 
        try:
            ibm_db.set_option(self.stmt_handler, 
                 {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC}, 0)
            if rowcount_prefetch:
                ibm_db.set_option(self.stmt_handler, 
                    {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH: ibm_db.SQL_ROWCOUNT_PREFETCH_ON}, 0)
        except Exception, inst:
            raise _get_exception(inst)
        self._is_scrollable_cursor = True
        self._result_set_produced = True
        if self.connection.dbms_name[0:3] != 'IDS':
            for column_index in range(num_columns):
                try:
                    type = ibm_db.field_type(self.stmt_handler, column_index)
                except Exception, inst:
                    raise _get_exception(inst)
                if type == "xml" or type == "clob" or type == "blob":
                    self._is_scrollable_cursor = False
                    ibm_db.set_option(self.stmt_handler, {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_FORWARD_ONLY}, 0)
                    #If the result set contains a LOBs, XML the cursor type will never be SQL_CURSOR_STATIC because DB2 does not allow this. (http://publib.boulder.ibm.com/infocenter/db2luw/v9r7/index.jsp?topic=/com.ibm.db2.luw.messages.sql.doc/doc/msql00270n.html)
                    if rowcount_prefetch:
                        ibm_db.set_option(self.stmt_handler, {ibm_db.SQL_ATTR_ROWCOUNT_PREFETCH: ibm_db.SQL_ROWCOUNT_PREFETCH_OFF}, 0)
                        #SQL_ATTR_ROWCOUNT_PREFETCH is not supported when the cursor contains LOBs or XML (http://publib.boulder.ibm.com/infocenter/db2luw/v9r7/index.jsp?topic=/com.ibm.db2.luw.apdv.cli.doc/doc/r0000644.html)
                    #print Warning("rowcount could not be updated because select includes xml, clob and/or blob type column(s)")
                    return True
        return True

    # Helper for executing an SQL statement.
    def _execute_helper(self, rows_counter, parameters=None):
        logger.debug('_execute_helper( '+repr(rows_counter)+', '+repr(parameters)+' )')
        if parameters is not None:
            buff = []
            CONVERT_STR = (datetime.datetime, datetime.date, datetime.time, buffer)
            # Convert date/time and binary objects to string for 
            # inserting into the database. 
            for param in parameters:
                if isinstance(param, CONVERT_STR):
                    param = str(param)
                buff.append(param)
            parameters = tuple(buff)
            try:                
                return_value = ibm_db.execute(self.stmt_handler, parameters)
                logger.debug('_execute_helper  (1)  return_value: '+str(return_value))
                if not return_value:
                    if ibm_db.conn_errormsg() is not None:
                        raise Error(str(ibm_db.conn_errormsg()))
                    if ibm_db.stmt_errormsg() is not None:
                        raise Error(str(ibm_db.stmt_errormsg()))
                if rows_counter is not None:
                    rows_counter.append(ibm_db.num_rows(self.stmt_handler))
            except Exception, inst:
                raise _get_exception(inst)
        else:
            try:
                return_value = ibm_db.execute(self.stmt_handler)
                logger.debug('_execute_helper  (2)  return_value: '+str(return_value))
                if not return_value:
                    if ibm_db.conn_errormsg() is not None:
                        raise Error(str(ibm_db.conn_errormsg()))
                    if ibm_db.stmt_errormsg() is not None:
                        raise Error(str(ibm_db.stmt_errormsg()))
                if rows_counter is not None:
                    rows_counter.append(ibm_db.num_rows(self.stmt_handler))
            except Exception, inst:
                raise _get_exception(inst)
        return return_value

    # This method is used to set the rowcount after executing an SQL 
    # statement. 
    def _set_rowcount(self):
        logger.debug('_set_rowcount()')
        self.__rowcount = 0
        if not self._result_set_produced:
            try:
                counter = ibm_db.num_rows(self.stmt_handler)
            except Exception, inst:
                raise _get_exception(inst)
            self.__rowcount = counter
        elif self._is_scrollable_cursor:
            try:
                counter = ibm_db.get_num_result(self.stmt_handler)
            except Exception, inst:
                raise _get_exception(inst)
            if counter >= 0:
                self.__rowcount = counter
        return True

    # Retrieves the last generated identity value from the DB2 catalog
    def _get_last_identity_val(self):
        """
        The result of the IDENTITY_VAL_LOCAL function is not affected by the following:
         - A single row INSERT statement with a VALUES clause for a table without an
        identity column
         - A multiple row INSERT statement with a VALUES clause
         - An INSERT statement with a fullselect

        """
        operation = 'SELECT IDENTITY_VAL_LOCAL() FROM SYSIBM.SYSDUMMY1'
        try:
            stmt_handler = ibm_db.prepare(self.conn_handler, operation)
            if ibm_db.execute(stmt_handler):
                row = ibm_db.fetch_assoc(stmt_handler)
                if row['1'] is not None:
                  identity_val = int(row['1'])
                else:
                  identity_val = None
            else:
                if ibm_db.conn_errormsg() is not None:
                    raise Error(str(ibm_db.conn_errormsg()))
                if ibm_db.stmt_errormsg() is not None:
                    raise Error(str(ibm_db.stmt_errormsg()))
        except Exception, inst:
            raise _get_exception(inst)
        return identity_val
    last_identity_val = property(_get_last_identity_val, None, None, "")

    def execute(self, operation, parameters=None):
        """
        This method can be used to prepare and execute an SQL 
        statement.  It takes the SQL statement(operation) and a 
        sequence of values to substitute for the parameter markers in  
        the SQL statement as arguments.
        """
        logger.debug('execute('+repr(operation)+', '+repr(parameters)+' )')
        if not (isinstance(operation, types.StringType) or isinstance(operation, types.UnicodeType)):
            raise InterfaceError("execute expects the first argument [%s] "
                                      "to be of type String or Unicode." % operation )
        if parameters is not None:
            if not isinstance(parameters, (types.ListType, types.TupleType, types.DictType)): 
                raise InterfaceError("execute parameters argument should be sequence.")
        self.__description = None
        self._all_stmt_handlers = []
        self._prepare_helper(operation)
        self._set_cursor_helper()
        self._execute_helper(None, parameters)
        return self._set_rowcount()

    def executemany(self, operation, seq_parameters):
        """
        This method can be used to prepare, and then execute an SQL 
        statement many times.  It takes the SQL statement(operation) 
        and sequence of sequence of values to substitute for the 
        parameter markers in the SQL statement as its argument.
        """
        logger.debug('executemany('+repr(operation)+', '+repr(seq_parameters)+' )')
        if not (isinstance(operation, types.StringType) or isinstance(operation, types.UnicodeType)):
            raise InterfaceError("executemany expects the first argument "
                                                    "to be of type String or Unicode.")
        if seq_parameters is None:
            raise InterfaceError("executemany expects a not None "
                                  "seq_parameters value")

        if not isinstance(seq_parameters, (types.ListType, types.TupleType)):
            raise InterfaceError("executemany expects the second argument "
                                  "to be of type list or tuple of sequence.")

        self.__description = None
        self._all_stmt_handlers = []
        self._prepare_helper(operation)
        rows_counter = []
        for index in range(len(seq_parameters)):
            self._execute_helper(rows_counter, seq_parameters[index])

        rowno = 0
        for rows in rows_counter:
           rowno += rows
        self.__rowcount = rowno
        return True

    def _fetch_helper(self, fetch_size=-1):
        """
        This method is a helper function for fetching fetch_size number of 
        rows, after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.
        If this is not provided it fetches all the remaining rows.
        """
        logger.debug('_fetch_helper('+repr(fetch_size)+')')
        if self.stmt_handler is None:
            raise ProgrammingError("Please execute an SQL statement in "
                                   "order to get a row from result set.")
        if self._result_set_produced == False:
            raise  ProgrammingError("The last call to execute did not "
                                              "produce any result set.")
        row_list = []
        rows_fetched = 0
        while (fetch_size == -1) or \
              (fetch_size != -1 and rows_fetched < fetch_size):
            try:
                row = ibm_db.fetch_tuple(self.stmt_handler)
                logger.debug('_fetch_helper('+ repr(row) +')')
            except Exception, inst:
                return row_list
            
            if row != False:
                row_list.append(self._fix_return_data_type(row))
            else:
                return row_list
            rows_fetched = rows_fetched + 1
        return row_list

    def fetchone(self):
        """This method fetches one row from the database, after 
        executing an SQL statement which produces a result set.
        
        """
        row_list = self._fetch_helper(1)
        if len(row_list) == 0:
            return None
        else:
            return row_list[0]

    def fetchmany(self, size=0):
        """This method fetches size number of rows from the database,
        after executing an SQL statement which produces a result set.
        It takes the number of rows to fetch as an argument.  If this 
        is not provided it fetches self.arraysize number of rows. 
        """
        logger.debug('fetchmany( size='+repr(size)+')')
        if not isinstance(size, (int, long)):
            raise InterfaceError( "fetchmany expects argument type int or long.")
        if size == 0:
            size = self.arraysize
        if size < -1:
            raise ProgrammingError("fetchmany argument size expected to be positive.")

        return self._fetch_helper(size)

    def fetchall(self):
        """This method fetches all remaining rows from the database,
        after executing an SQL statement which produces a result set.
        """
        return self._fetch_helper()

    def nextset(self):
        """This method can be used to get the next result set after 
        executing a stored procedure, which produces multiple result sets.
        """
        if self.stmt_handler is None:
            raise ProgrammingError("Please execute an SQL statement in "
                                             "order to get result sets.")
        if self._result_set_produced == False:
            raise ProgrammingError("The last call to execute did not "
                                             "produce any result set.")
        try:
            # Store all the stmt handler that were created.  The 
            # handler was the one created by the execute method.  It 
            # should be used to get next result set. 
            self._all_stmt_handlers.append(self.stmt_handler)
            self.stmt_handler = ibm_db.next_result(self._all_stmt_handlers[0])
        except Exception, inst:
            raise _get_exception(inst)

        if self.stmt_handler == False:
            self.stmt_handler = None
        if self.stmt_handler == None:
            return None 
        return True

    def setinputsizes(self, sizes):
        """This method currently does nothing."""
        pass

    def setoutputsize(self, size, column=-1):
        """This method currently does nothing."""
        pass

    # This method is used to convert a string representing date/time 
    # and binary data in a row tuple fetched from the database 
    # to date/time and binary objects, for returning it to the user.
    def _fix_return_data_type(self, row):
        row = list(row)
        logger.debug('_fix_return_data_type( '+repr(row)+' )')
        for index in range(len(row)):
            if row[index] is not None:
                type = ibm_db.field_type(self.stmt_handler, index)
                type = type.upper()

                try:
                    if type == 'TIMESTAMP':
                        # strptime() method does not support 
                        # microsecond format. 
                        microsec = 0
                        if row[index][20:] != '':
                            microsec = int(row[index][20:])
                            row[index] = row[index][:19]
                        row[index] = datetime.datetime.strptime(row[index],
                                                          '%Y-%m-%d %H:%M:%S')
                        row[index] = row[index].replace(
                                                       microsecond = microsec)
                    if type == 'DATE':
                        row[index] = datetime.datetime.strptime(row[index], 
                                                            '%Y-%m-%d').date()
                    if type == 'TIME':
                        row[index] = datetime.datetime.strptime(row[index],
                                                            '%H:%M:%S').time()
                    if type == 'BLOB':
                        row[index] = buffer(row[index])

                    if type == 'REAL':
                        row[index] = decimal.Decimal(str(row[index]).replace(",","."))    

                except Exception, inst:
                    raise DataError("Data type format error: "+ str(inst))
        return tuple(row)
