"""
Connector class to connect to Snowflake
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

def get_engine(warehouse,database,account,role,user_name,password_key):
    """
    Establishes connection to a Snowflake Server

    Gets sqlalchemy engine
    :param password_key:
    :return:
    """

    with open(password_key, "rb") as key:
        p_key= serialization.load_pem_private_key(key.read(), password=None, backend=default_backend())

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    _engine = create_engine(URL(
                account = account,
                user = user_name,
                role = role,
                warehouse = warehouse,
                database = database),
                connect_args={
                    'private_key': pkb,
                    }
                )
    return _engine