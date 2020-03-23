import settings
import pymysql
from flask import abort, request, session
from pymysql.cursors import DictCursor
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *

def use_db(func):
    def wrapper(*args, **kwargs):
        try:
            dbConnection = pymysql.connect(settings.MYSQL_HOST,
                                settings.MYSQL_USER,
                                settings.MYSQL_PASSWD,
                                settings.MYSQL_DB,
                                charset='utf8mb4',
                                cursorclass=DictCursor)
            cursor = dbConnection.cursor()
            kwargs['cursor'] = cursor
            return func(*args, **kwargs)
        except:
            abort(404)
        finally:
            cursor.close()
            dbConnection.close()
    return wrapper

def get_user(cursor, user_id):
    cursor.callproc('getUserById', (user_id,))
    return cursor.fetchone()

def get_ldapConnection(username, password):
    ldapServer = Server(host=settings.LDAP_HOST)
    return Connection(ldapServer,
        raise_exceptions=True,
        user='uid={username}, ou=People,ou=fcs,o=unb'.format(username=username),
        password=password)

def get_vals(d, *args):
    return tuple(d[arg] for arg in args)

def uri(url, id):
    return '{url}/{id}'.format(url=url, id=id)
