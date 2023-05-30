import argparse
from flask import Flask, jsonify
from models.models import (
    DataProviders, Benefits, 
    Carriers, Dates, Insured,
    Policies, DATABASE_URL, engine
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database import Database
from read_data import PopulateDatabaseTables


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/policy-info/<string:number>', methods=['GET'])
def get_policy_info(number):
    '''return the effective_date, issue_date, maturity_date, death_benefit, and carrier_name'''
    policy = session.query(Policies).filter(Policies.policy_id==number).first()
    effective = session.query(Dates.date_value).filter(Dates.date_id == policy.effective_date).first()
    issue = session.query(Dates.date_value).filter(Dates.date_id == policy.issue_date).first()
    maturity = session.query(Dates.date_value).filter(Dates.date_id == policy.maturity_date).first()
    benefit = session.query(Benefits.death_benefit).filter(Benefits.benefit_id == policy.benefits_id).first()
    carrier = session.query(Carriers.carrier_name).filter(Carriers.carrier_id == policy.carrier_id).first()
    dates = [effective, issue, maturity]
    others = [benefit, carrier]
    if policy:
        for i in range(3):
            if dates[i] != None:
                dates.append(dates[i][0].strftime('%Y-%m-%d'))
            else:
                dates.append(None)
       
        for o in range(2):
            if o != None:
                others.append(others[o][0])
            else:
                others.append(None)

        policy_info = {
            'effective_date': dates[-3],
            'issue_date': dates[-2],
            'maturity_date': dates[-1],
            'death_benefit': others[-2],
            'carrier_name': others[-1],
        }
        return jsonify(policy_info)
    else:
        return jsonify({'error': 'Policy not found'})

@app.route('/carrier-policy-count/<string:carrier_name>', methods=['GET'])
def get_carrier_count(carrier_name):
    '''return the count of all unique policies we have from that carrier'''
    carrier_id = session.query(Carriers.carrier_id).filter(Carriers.carrier_name==carrier_name).all()
    if carrier_id:
        policies = session.query(func.count(Policies.policy_id)).filter(Policies.carrier_id == carrier_id[0][0]).scalar()
        if policies:
            policy_count = {
                'carrier_name': carrier_name,
                'policy_count': policies,
            }
            return jsonify(policy_count)
        else:
            return jsonify({'error': f'{carrier_name} has no policies with us'})
    else:
        return jsonify({'error': f'{carrier_name} not found'})
    
@app.route('/person-policies/<string:person_name>', methods=['GET'])
def get_person_policies(person_name):
    '''
        return a list of all policies for that person regardless the position 
        (primary or secondary) of the person on the policy
    '''
    person_id = session.query(Insured.insured_id).filter(Insured.insured_name==person_name).all()
    if person_id:
        count_dict = dict()
        for id in person_id:
            name_id = f'{person_name}-{id[0]}'
            policies = session.query(Policies.policy_id).filter(
                Policies.insured1_id.in_(id) | Policies.insured2_id.in_(id)).all()
            if policies:
                count_dict[name_id] = [pol[0] for pol in policies]
            else:
                count_dict[name_id] = None
        policies_ids = {
            'policies': count_dict
        }
        return jsonify(policies_ids)
    else:
        return jsonify({'error': f'{person_name} not found'})

@app.route('/data-provider-policies/<string:provider_code>', methods=['GET'])
def get_provider_policies_count(provider_code):
    '''return the count of all policies that we have information on from that data provider'''
    provider_id = session.query(DataProviders.provider_id).filter(DataProviders.code==provider_code).first()
    if provider_id:
        policies = session.query(func.count(Policies.policy_id)).filter(Policies.provider_id == provider_id[0]).scalar()
        if policies:
            policies_ids = {
                'policies': policies
            }
            return jsonify(policies_ids)
        else:
            return jsonify({'error': f'{provider_code} has no policies with us'})
    else:
        return jsonify({'error': f'{provider_code} not found'})

@app.route('/')
def hello():
    '''fun opening path'''
    return 'Hello, World!'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    '''just in case the path is incorrect'''
    if 'policy' in path:
        return f'You want path: policy-info/ or carrier-policy-count/'
    elif 'info' in path:
        return f'You want path: policy-info/'
    elif 'provider' in path:
        return f'You want path: data-provider-policies/'
    elif 'person' in path:
        return f'You want path: person-policies/'
    elif 'carrier' in path:
        return f'You want path: carrier-policy-count/'
    elif 'count' in path:
        return f'You want path: carrier-policy-count/'
    elif 'policies' in path:
        return f'You want path: data-provider-policies/ or person-policies/'
    else:
        return 'Congradulations! This path does not exist. Talk to the devs to get it created.'



if __name__ == '__main__':
    '''if True is passed into the Database class the tables were be removed'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="csv_file", help="path to CSV file")
    args = parser.parse_args()
    d = Database()
    d.main()
    p = PopulateDatabaseTables(args.csv_file)
    p.populate_tables()
    app.run(port=5000)
