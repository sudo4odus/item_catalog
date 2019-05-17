#!/usr/bin/python
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

"""Users class <==> users table"""

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    picture = Column(String(256))
    
    

"""Programs class <==> programs table"""

class Programs(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, default=1)
    users = relationship(Users)

    @property
    def serialize(self):
        # Return object data in serializeable format
        return {
            'id': self.id,
            'title': self.name,
        }


"""Courses class <==> courses table"""

class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String(512))
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    programs = relationship(Programs)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, default=1)
    users = relationship(Users)

    @property
    def serialize(self):
        # Return object data in serializeable format
        return {
            'id': self.id,
            'program_id': self.program_id,
            'title': self.title,
            'description': self.description,
        }

engine = create_engine('sqlite:///udacity_courses.db')
Base.metadata.create_all(engine)
