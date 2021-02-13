# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_sql_expressions.htm
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
meta = MetaData()

engine = create_engine('sqlite:///:memory:', echo=True)


metadata = MetaData()
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
    Column('password', String)
)

metadata.create_all(engine)