import argparse
import pandas as pd
import numpy as np
from models.models import (
    DataProviders, Benefits, 
    Carriers, Dates, Insured,
    Policies, engine
)
from sqlalchemy.orm import sessionmaker
from pandas_validator import ColumnsValidator
from sqlalchemy import inspect


class CustomValidator(ColumnsValidator):
        def __init__(self, df):
            super().__init__(df)
            self.rules = []
            self.df = df
            
        
        def add_rule(self, column_name, rule):
            self.rules.append((column_name, rule))

        def add(self, column_name, rule):
            self.add_rule(column_name, rule)
        
        def validate(self):
            for column_name, rule in self.rules:
                self.df[column_name].astype(rule)
        


class PopulateDatabaseTables:


    def __init__(self, csv_file):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.path = csv_file

        # Load data from a CSV file
        self.df = pd.read_csv(self.path)
        self.df = self.df.where(pd.notna(self.df), None)
        self.valid_df()


    def valid_df(self):
        '''Encodes each column with a set data type'''
        validator = CustomValidator(self.df)
        for column in self.df:
            if column in ('data_provider_priority', 'origination_death_benefit'):
                t = int
            elif 'date' in column:
                t = np.datetime64
            else:
                t = str
            validator.add(column, t)
        validator.validate()

    def already_in_database(self, table):
        return self.session.query(table).filter_by().first()

    def put_in_db(self, tgt_model, tgt_table):
        '''Adds the data into the tables and returns the created id'''
        inspector = inspect(type(tgt_model))
        columns = [column.name for column in inspector.columns]
        if 'date_value' in columns and type(tgt_model.date_value) != str and tgt_table == 'dates':
            return None
        self.session.add(tgt_model)
        self.session.commit()
        self.session.flush()
        
        id = next((column for column in columns if 'id' in column), None)
        tgt_id = tgt_model.__getattribute__(id)
        return tgt_id

    def populate_tables(self):
        '''Loops through each row of df and populates the tables with that data'''
        for _, row in self.df.iterrows():
            

            # confirm is policy
            # confirm is provider
            # confirm is date
            # confirm is insured
            # confirm is benefit
            # confirm is carrier
            # if confirmed save id and continue
            # will return None if not in table
            policy_in_db = self.session.query(Policies.policy_id).filter(Policies.policy_id==row['number']).first()
            
            if not policy_in_db:
                policy = Policies(policy_id=row['number'])
                provider_db_id = self.put_in_db(policy, 'policy')
                policy_db_id = row['number']
            
            provider_in_db = self.session.query(DataProviders.provider_id).filter(DataProviders.code == row['data_provider_code'],
                                                DataProviders.name == row['data_provider_description'], 
                                                DataProviders.priority == row['data_provider_priority']).first()
            
            if not provider_in_db and row['data_provider_code'] != None:
                provider = DataProviders(priority=row['data_provider_priority'], code=row['data_provider_code'], name=row['data_provider_description'])
                provider_db_id = self.put_in_db(provider, 'provider')
            else:
                if provider_in_db != None:
                    provider_db_id = provider_in_db[0]
                else:
                    provider_db_id = provider_in_db
            
            e_date_in_db = self.session.query(Dates.date_id).filter(Dates.date_value == row['effective_date'] if type(row['effective_date']) == str else None).first()
            
            if not e_date_in_db and row['effective_date'] != None:
                e_dates = Dates(date_value=row['effective_date'] if row['effective_date'] != '' else None)
                e_dates_id = self.put_in_db(e_dates, 'date')
            else:
                if e_date_in_db != None:
                    e_dates_id = e_date_in_db[0]
                else:
                    e_dates_id = e_date_in_db

            i_date_in_db = self.session.query(Dates.date_id).filter(Dates.date_value == row['issue_date'] if type(row['issue_date']) == str else None).first()
            
            if not i_date_in_db and row['issue_date'] != None:
                i_dates = Dates(date_value=row['issue_date'] if row['issue_date'] != '' else None)
                i_dates_id = self.put_in_db(i_dates, 'date')
            else:
                if i_date_in_db != None:
                    i_dates_id = i_date_in_db[0]
                else:
                    i_dates_id = i_date_in_db

            m_date_in_db = self.session.query(Dates.date_id).filter(Dates.date_value == row['maturity_date'] if type(row['maturity_date']) == str else None).first()
            
            if not m_date_in_db and row['maturity_date'] != None:
                m_dates = Dates(date_value=row['maturity_date'] if row['maturity_date'] != '' else None)
                m_dates_id = self.put_in_db(m_dates, 'date')
            else:
                if m_date_in_db != None:
                    m_dates_id = m_date_in_db[0]
                else:
                    m_dates_id = m_date_in_db

            d1_date_in_db = self.session.query(Dates.date_id).filter(Dates.date_value == row['birth_date_1'] if type(row['birth_date_1']) == str else None).first()
            
            if not d1_date_in_db and row['birth_date_1'] != None:
                d1_dates = Dates(date_value=row['birth_date_1'] if row['birth_date_1'] != '' else None)
                d1_dates_id = self.put_in_db(d1_dates, 'date')
            
            if d1_date_in_db != None:
                d1_dates_id = d1_date_in_db[0]
            else:
                d1_dates_id = d1_date_in_db

            
            
            d2_date_in_db = self.session.query(Dates.date_id).filter(Dates.date_value == row['birth_date_2'] if type(row['birth_date_2']) == str else None).first()
            
            if not d2_date_in_db and row['birth_date_2'] != None:
                d2_dates = Dates(date_value=row['birth_date_2'] if row['birth_date_2'] != '' else None)
                d2_dates_id = self.put_in_db(d2_dates, 'date')

            if d2_date_in_db != None:
                d2_dates_id = d2_date_in_db[0]
            else:
                d2_dates_id = d2_date_in_db

            insured1_in_db = self.session.query(Insured.insured_id).filter(Insured.insured_name == row['name_1'], 
                                                                                            Insured.gender == row['gender_1'], 
                                                                                            Insured.dob == d1_dates_id).first()
            
            if not insured1_in_db and (row['name_1'] != None or row['gender_1'] != None or d1_dates_id):
                insured1s_in_db = Insured(insured_name=row['name_1'], gender=row['gender_1'], dob=d1_dates_id)
                insured1s_in_db_id = self.put_in_db(insured1s_in_db, 'insured')
            else:
                if insured1_in_db != None:
                    insured1s_in_db_id = insured1_in_db[0]
                else:
                    insured1s_in_db_id = insured1_in_db

            insured2_in_db = self.session.query(Insured.insured_id).filter(Insured.insured_name == row['name_2'] if type(row['name_2']) == str else None,
                                                                                            Insured.gender == row['gender_2'],
                                                                                            Insured.dob == d2_dates_id).first()
            
            if not insured2_in_db and (row['name_2'] != None or row['gender_2'] != None or d2_dates_id):
                insured2s_in_db = Insured(insured_name=row['name_2'], gender=row['gender_2'], dob=d2_dates_id)
                insured2s_in_db_id = self.put_in_db(insured2s_in_db, 'insured')
            else:
                if insured2_in_db != None:
                    insured2s_in_db_id = insured2_in_db[0]
                else:
                    insured2s_in_db_id = insured2_in_db
            
            benefit_in_db = self.session.query(Benefits.benefit_id).filter(Benefits.death_benefit == row['origination_death_benefit']).first()
            
            if not benefit_in_db and row['origination_death_benefit'] != None:
                benefits_in_db = Benefits(death_benefit=row['origination_death_benefit'])
                benefits_in_db_id = self.put_in_db(benefits_in_db, 'benefit')
            else:
                if benefit_in_db != None:
                    benefits_in_db_id = benefit_in_db[0]
                else:
                    benefits_in_db_id = benefit_in_db
            
            carriers_in_db = self.session.query(Carriers.carrier_id).filter(Carriers.carrier_name == row['carrier_name']).first()

            if not carriers_in_db and row['carrier_name'] != None:
                carriers_in_db = Carriers(carrier_name=row['carrier_name'])
                carriers_in_db_id = self.put_in_db(carriers_in_db, 'carriers')
            else:
                if carriers_in_db != None:
                    carriers_in_db_id = carriers_in_db[0]
                else:
                    carriers_in_db_id = carriers_in_db

            # update policy to have ids
            self.session.query(Policies).filter(
                Policies.policy_id == row['number']).update(
                    {'benefits_id': benefits_in_db_id, 
                    'carrier_id': carriers_in_db_id,
                    'insured1_id': insured1s_in_db_id,
                    'insured2_id': insured2s_in_db_id,
                    'provider_id': provider_db_id, 
                    'effective_date': e_dates_id,
                    'issue_date': i_dates_id,
                    'maturity_date': m_dates_id}) 
            
            self.session.commit()

            # update insured dob
            (self.session.query(Insured).filter(Insured.insured_id == insured1s_in_db_id)
            .update({'dob': d1_dates_id}))
            
            self.session.commit()

            (self.session.query(Insured).filter(Insured.insured_id == insured2s_in_db_id)
            .update({'dob': d2_dates_id}))
            
            self.session.commit()
        
        self.session.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="csv_file", help="path to CSV file")
    args = parser.parse_args()
    p = PopulateDatabaseTables(args.csv_file)
    p.populate_tables()
