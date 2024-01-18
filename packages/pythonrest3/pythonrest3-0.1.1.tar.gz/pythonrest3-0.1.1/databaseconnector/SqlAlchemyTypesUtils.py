import sys
import os


################################################ SaAuSQLTypes
def get_sa_AuSQL_string_types_list():
    return ['String', 'TIMESTAMP', 'timestamp', 'TIME', 'Time', 'Date', 'JSON', 'DateTime',
            'CHAR',  'DATE', 'DATETIME', 'Enum', 'Interval', 'NCHAR', 'NVARCHAR',
            'TEXT', 'Text', 'Unicode', 'UnicodeText', 'VARCHAR']


def get_sa_AuSQL_bytes_types_list():
    return ['Binary', 'BLOB', 'BINARY', 'CLOB', 'LargeBinary', 'VARBINARY']


def get_sa_AuSQL_int_types_list():
    return ['Integer', 'BIGINT', 'BigInteger',
            'INTEGER', 'SMALLINT', 'SmallInteger']


def get_sa_AuSQL_float_types_list():
    return ['Float', 'DECIMAL', 'FLOAT', 'NUMERIC', 'Numeric', 'REAL']


def get_sa_AuSQL_bool_types_list():
    return ['Boolean', 'BOOLEAN']


def get_sa_AuSQL_list_types_list():
    return ['ARRAY']


def get_sa_AuSQL_dict_types_list():
    return []


################################################ SaMaSQLTypes
def get_sa_MaSQL_string_types_list():
    return ['String', 'TIMESTAMP', 'timestamp', 'TIME', 'Time', 'Date', 'JSON', 'DateTime',
            'CHAR',  'DATE', 'DATETIME', 'Enum', 'Interval', 'NCHAR', 'NVARCHAR',
            'TEXT', 'Text', 'Unicode', 'UnicodeText', 'VARCHAR']


def get_sa_MaSQL_bytes_types_list():
    return ['Binary', 'BLOB', 'BINARY', 'CLOB', 'LargeBinary', 'VARBINARY']


def get_sa_MaSQL_int_types_list():
    return ['Integer', 'BIGINT', 'BigInteger',
            'INTEGER', 'SMALLINT', 'SmallInteger']


def get_sa_MaSQL_float_types_list():
    return ['Float', 'DECIMAL', 'FLOAT', 'NUMERIC', 'Numeric', 'REAL']


def get_sa_MaSQL_bool_types_list():
    return ['Boolean', 'BOOLEAN']


def get_sa_MaSQL_list_types_list():
    return ['ARRAY']


def get_sa_MaSQL_dict_types_list():
    return []


################################################ SaMySQLTypes
def get_sa_MySQL_string_types_list():
    return ['String', 'TIMESTAMP', 'timestamp', 'TIME', 'Time', 'Date', 'JSON', 'DateTime',
            'CHAR',  'DATE', 'DATETIME', 'Enum', 'Interval', 'NCHAR', 'NVARCHAR', "YEAR", "year",
            'TEXT', 'Text', 'Unicode', 'UnicodeText', 'VARCHAR']


def get_sa_MySQL_bytes_types_list():
    return ['Binary', 'BLOB', 'BINARY', 'CLOB', 'LargeBinary', 'VARBINARY']


def get_sa_MySQL_int_types_list():
    return ['Integer', 'BIGINT', 'BigInteger',
            'INTEGER', 'SMALLINT', 'SmallInteger', 'int']


def get_sa_MySQL_float_types_list():
    return ['Float', 'DECIMAL', 'FLOAT', 'NUMERIC', 'Numeric', 'REAL']


def get_sa_MySQL_bool_types_list():
    return ['Boolean', 'BOOLEAN']


def get_sa_MySQL_list_types_list():
    return ['ARRAY']


def get_sa_MySQL_dict_types_list():
    return []


################################################ SaOcSQLTypes
def get_sa_OcSQL_string_types_list():
    return ['CHAR', 'VARCHAR2', 'VARCHAR', ]


def get_sa_OcSQL_bytes_types_list():
    return ['Binary', 'BINARY', 'LargeBinary', 'VARBINARY',
            'NCLOB', 'BFILE', 'CLOB', 'BLOB', 'LONG', 'RAW', 'LONG RAW']


def get_sa_OcSQL_int_types_list():
    return ['Integer', 'BIGINT', 'BigInteger',
            'INTEGER', 'SMALLINT', 'SmallInteger']


def get_sa_OcSQL_float_types_list():
    return ['Float', 'DECIMAL', 'FLOAT', 'NUMERIC', 'Numeric', 'REAL']


def get_sa_OcSQL_bool_types_list():
    return ['Boolean', 'BOOLEAN']


def get_sa_OcSQL_list_types_list():
    return ['ARRAY']


def get_sa_OcSQL_dict_types_list():
    return []


################################################ SaPgSQLTypes
def get_sa_PgSQL_string_types_list():
    return ['character varying', 'char', 'BLOB', 'character', 'varchar', 'Binary',
            'name', 'CLOB', 'DATE', 'DATETIME', 'Enum', 'Interval', 'LargeBinary',
            'text', 'Unicode', 'UnicodeText', 'VARBINARY', 'UUID', 'date', 'time without time zone',
            'timestamp with time zone', 'timestamp without time zone', 'timestamp', 'jsonb', 'JSONB', 'inet', 'INET']


def get_sa_PgSQL_bytes_types_list():
    return ['bytea']


def get_sa_PgSQL_int_types_list():
    return ['smallint', 'integer', 'bigint', 'serial', 'bigserial', 'oid', 'regprocregproc',
            'regprocedure', 'regoper', 'regoperator', 'regclass', 'regtype']


def get_sa_PgSQL_float_types_list():
    return ['decimal', 'numeric', 'real', 'double precision', 'money']


def get_sa_PgSQL_bool_types_list():
    return ['bool', 'boolean']


def get_sa_PgSQL_list_types_list():
    return ['ARRAY', 'GEOMETRY', 'array', 'geometry']


def get_sa_PgSQL_dict_types_list():
    return []


################################################ SaSeSQLTypes
def get_sa_SeSQL_string_types_list():
    return ['char', 'varchar', 'text', 'nchar', 'nvarchar', 'ntext', 'date', 'smalldatetime', 'datetime', 'datetime2', 'datetimeoffset', 'time']


def get_sa_SeSQL_bytes_types_list():
    return ['binary', 'varbinary', 'image']


def get_sa_SeSQL_int_types_list():
    return ['bigint', 'numeric', 'bit', 'smallint', 'decimal', 'smallmoney', 'int', 'tinyint', 'money']


def get_sa_SeSQL_float_types_list():
    return ['float', 'real']


def get_sa_SeSQL_bool_types_list():
    return ['BOOL', 'bool', 'BOOLEAN', 'boolean']


def get_sa_SeSQL_list_types_list():
    return ['array']


def get_sa_SeSQL_dict_types_list():
    return []

########################################################################################################################
def get_sa_string_types_list():
    return ['String', 'TIMESTAMP', 'timestamp', 'TIME', 'Time', 'Date', 'JSON', 'jsonb', 'JSONB' 'DateTime',
            'CHAR',  'DATE', 'DATETIME', 'Enum', 'Interval', 'NCHAR', 'NVARCHAR', 'UUID',
            'TEXT', 'Text', 'Unicode', 'UnicodeText', 'VARCHAR', "YEAR", "year"]


def get_sa_bytes_types_list():
    return ['Binary', 'BLOB', 'BINARY', 'CLOB', 'LargeBinary', 'VARBINARY']


def get_sa_int_types_list():
    return ['Integer', 'BIGINT', 'BigInteger',
            'INTEGER', 'SMALLINT', 'SmallInteger', 'bigint']


def get_sa_float_types_list():
    return ['Float', 'DECIMAL', 'FLOAT', 'NUMERIC', 'Numeric', 'REAL']


def get_sa_bool_types_list():
    return ['Boolean', 'BOOLEAN']


def get_sa_list_types_list():
    return ['ARRAY']


def get_sa_dict_types_list():
    return []


def type_with_size(column_type):
    return True if '(' in column_type and ')' in column_type else False


def add_size_to_result(result, column_type):
    return result + column_type[column_type.index('('):]


def get_sa_type_match(type_list, column_type_no_size, python_type_value, python_type):
    first_result = next((sa_type for sa_type in type_list
                        if sa_type.lower() == column_type_no_size.lower() and python_type_value == python_type), None)
    if first_result:
        return first_result

    contains_list = [sa_type for sa_type in type_list
                        if sa_type.lower() in column_type_no_size.lower() and python_type_value == python_type]

    if contains_list != list():
        result = max(contains_list, key=len)
        return result

    third_result = next((sa_type for sa_type in type_list if python_type_value == python_type), None)
    if third_result:
        return third_result


def get_sa_type(column_type, python_type_value):

    column_type_no_size = column_type[:column_type.index('(')] if '(' in column_type else column_type

    str_type_list = get_sa_string_types_list()
    bytes_type_list = get_sa_bytes_types_list()
    int_type_list = get_sa_int_types_list()
    float_type_list = get_sa_float_types_list()
    bool_type_list = get_sa_bool_types_list()
    list_type_list = get_sa_list_types_list()
    dict_type_list = get_sa_dict_types_list()

    types_list_object = {'str': str_type_list, 'bytes': bytes_type_list, 'int': int_type_list, 'float': float_type_list,
                        'bool': bool_type_list, 'list': list_type_list, 'dict': dict_type_list}

    executed_script_name = os.path.basename(sys.argv[0])

    for python_type, type_list in types_list_object.items():
        result = get_sa_type_match(type_list, column_type_no_size, python_type_value, python_type)
        if result:
            if type_with_size(column_type):
                if column_type_no_size == "int" or column_type_no_size == "bigint" and executed_script_name == 'mysql_script.py':
                    pass
                else:
                    result = add_size_to_result(result, column_type)
            return result
