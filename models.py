from datetime import timedelta
from flask import Flask, render_template, request, jsonify ,session as ss ,json
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    email = Column('email', String)
    password = Column('password', String)
    status =  Column('status', String)

    def __init__(self, firstname, lastname,email, password, status="simple"):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.status = status

class Course(Base):
    __tablename__ = "courses"

    id_c = Column('id_с', Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description
        }
