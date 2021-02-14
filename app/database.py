import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import User, Hackathon, Skill

Base = declarative_base()

engine = create_engine(
    'cockroachdb://{}:{}@{}:26257/{}.hack?sslmode=verify-full&sslrootcert={}'.format(os.environ['username'], os.environ['password'], os.environ['globalhost'], os.environ['cluster'], os.environ['certpath']),
    echo=True                   # Log SQL queries to stdout
)

Base.metadata.create_all(engine)

def get_users():
    factory = sessionmaker(bind=engine)
    session = factory()
    users = session.query(User).all()
    return users


def create_users(user):
    factory = sessionmaker(bind=engine)
    session = factory()
    new_user = User(name=user['name'], email=user['email'], password=user['password'])
    for skill in user['skills']:
        skillRecord = session.query(Skill).filter(Skill.name == skill).first()
        new_user.skills.append(skillRecord)
    for hackathon in user['hackathons']:
        hackathonRecord = session.query(Hackathon).filter(Hackathon.name == hackathon).first()
        new_user.hackathons.append(hackathonRecord)
    session.add(new_user)
    session.commit()
    return new_user
