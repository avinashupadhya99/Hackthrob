from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
import os

Base = declarative_base()

engine = create_engine(
    'cockroachdb://{}:{}@{}:26257/{}.hack?sslmode=verify-full&sslrootcert={}'.format(os.environ['username'], os.environ['password'], os.environ['globalhost'], os.environ['cluster'], os.environ['certpath']),
    echo=True                   # Log SQL queries to stdout
)

user_skills_table = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class User(Base):
    """The User class corresponds to the "users" database table.
    """
    __tablename__ = 'users'
    id      = Column(Integer, primary_key=True)
    name    = Column(String(50))       
    email = Column(String(50), unique=True)
    password = Column(String(25))
    children = relationship("Skill", secondary=user_skills_table)

class Skill(Base):
    __tablename__ = 'skills'
    id   = Column(Integer, primary_key=True)
    name = Column(String(15))




Base.metadata.create_all(engine)