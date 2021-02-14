from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
import os

Base = declarative_base()

engine = create_engine(
    'cockroachdb://{}:{}@{}:26257/{}.hack?sslmode=verify-full&sslrootcert={}'.format(os.environ['username'], os.environ['password'], os.environ['globalhost'], os.environ['cluster'], os.environ['certpath']),
    echo=True                   # Log SQL queries to stdout
)

def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d")]

user_skills_table = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

user_hackathons_table = Table('user_hackathons', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('hackathon_id', Integer, ForeignKey('hackathons.id'))
)

class User(Base):
    """The User class corresponds to the "users" database table.
    """
    __tablename__ = 'users'
    id      = Column(Integer, primary_key=True)
    name    = Column(String(75))       
    email = Column(String(50), unique=True)
    password = Column(String(25))
    skills = relationship("Skill", secondary=user_skills_table)
    hackathons = relationship("Hackathon", secondary=user_hackathons_table)

    def __init__(self, id, name, email, password, skills, hackathons):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.skills = skills
        self.hackathons = hackathons
        pass

    @property
    def serialize(self):
        return {
            'id'         : self.id,
            'name'       : self.name,
            'email'      : self.email,
            'skills'  : self.serialize_skills,
            'hackathons': self.serialize_hackathons
        }
    @property
    def serialize_skills(self):
       return [ item.serialize for item in self.skills]

    @property
    def serialize_hackathons(self):
       return [ item.serialize for item in self.hackathons]

class Skill(Base):
    __tablename__ = 'skills'
    id   = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, id, name):
        self.id = id
        self.name = name
        pass

    @property
    def serialize(self):
        return {
            'id'         : self.id,
            'name'       : self.name
        }

class Hackathon(Base):
    __tablename__ = 'hackathons'
    id   = Column(Integer, primary_key=True)
    name = Column(String(30))
    start = Column(Date)
    end = Column(Date)

    def __init__(self, id, name, start, end):
        self.id = id
        self.name = name
        self.start = start
        self.end = end
        pass

    @property
    def serialize(self):
        return {
            'id'    : self.id,
            'name'  : self.name,
            'start' : dump_date(self.start),
            'end'   : dump_date(self.end)
        }





Base.metadata.create_all(engine)