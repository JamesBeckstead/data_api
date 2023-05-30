from sqlalchemy import (
    create_engine, Column, 
    Date, Integer, String, 
    DateTime, ForeignKey)
from sqlalchemy.orm import declarative_base, relationship, Query
from datetime import datetime



DATABASE_URL = 'postgresql://temp:temp@localhost/james_preston?options=-c%20search_path=homework'

engine = create_engine(DATABASE_URL)

Base = declarative_base()

'''
    This schema creates a central table (policies) that holds the policy id, 
    a unique value, and references other tables for all other details.
'''

class DataProviders(Base):
    '''
        This table holds the providers details:+
        - name
        - code
        - priority
            ex. 
                POP, Popular Underwriting, 3
    '''
    __tablename__ = 'data_providers'
    provider_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    code = Column(String(100))
    priority = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    query_class = Query
    

class Benefits(Base):
    '''
        This table holds the benfit amount
            ex.
                2000000
    '''
    __tablename__ = 'benefits'
    benefit_id = Column(Integer, primary_key=True, autoincrement=True)
    death_benefit = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    query_class = Query
    


class Carriers(Base):
    '''
        This table holds all the carrier details
        - carrier name
            ex.
                Equitable Financial
                AXA
    '''
    __tablename__ = 'carriers'
    carrier_id = Column(Integer, primary_key=True, autoincrement=True)
    carrier_name = Column(String(150))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    query_class = Query
    


class Dates(Base):
    '''
        This holds all dates from the policy
        - date_value

            ex.
                8/29/1933
                2/27/2008
                3/20/2008
    '''
    __tablename__ = 'dates'
    date_id = Column(Integer, primary_key=True, autoincrement=True)
    date_value = Column(Date, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    query_class = Query


class Insured(Base):
    '''
        This table holds the insured persons details
        - genger
        - insured name
        - dob (date of birth) - this is a reference to dates table

            ex.
                Bradley Martin, F, 111

    '''
    __tablename__ = 'insured'
    insured_id = Column(Integer, primary_key=True, autoincrement=True)
    insured_name = Column(String(500))
    gender = Column(String(10))
    dob = Column(Integer, ForeignKey("dates.date_id"), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    births = relationship('Dates', backref='birth_date') 

    query_class = Query
    
    

class Policies(Base):
    '''
        This table holds the references needed to reconstruct the policy.
        This table holds the policy number, a unique value, and 
        references all other details.

        note: the dates are ids as well
            
            ex.
                39P5UYYYY
                77777XKDD
    '''
    __tablename__ = 'policies'
    policy_id = Column(String, primary_key=True)
    benefits_id = Column(Integer, ForeignKey("benefits.benefit_id"), nullable=True)
    carrier_id = Column(Integer, ForeignKey("carriers.carrier_id"), nullable=True)
    insured1_id = Column(Integer, ForeignKey("insured.insured_id"), nullable=True)
    insured2_id = Column(Integer, ForeignKey("insured.insured_id"), nullable=True)
    provider_id = Column(Integer, ForeignKey("data_providers.provider_id"), nullable=True)
    effective_date = Column(Integer, ForeignKey("dates.date_id"), nullable=True)
    issue_date = Column(Integer, ForeignKey("dates.date_id"), nullable=True)
    maturity_date = Column(Integer, ForeignKey("dates.date_id"), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    query_class = Query
