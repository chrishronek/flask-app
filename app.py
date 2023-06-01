from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Policy(db.Model):
    __tablename__ = 'life_policy'

    policy_key = db.Column(db.String(80), primary_key=True)
    number = db.Column(db.String(80), unique=True, nullable=False)
    data_provider_code = db.Column(db.String(80), unique=False, nullable=False)
    data_provider_description = db.Column(db.String(120), unique=False, nullable=False)
    effective_date = db.Column(db.String(120), unique=False, nullable=False)
    issue_date = db.Column(db.String(120), unique=False, nullable=False)
    maturity_date = db.Column(db.String(120), unique=False, nullable=False)
    origination_death_benefit = db.Column(db.String(120), unique=False, nullable=False)
    carrier_name = db.Column(db.String(120), unique=False, nullable=False)
    name_1 = db.Column(db.String(120), unique=False, nullable=False)
    gender_1 = db.Column(db.String(120), unique=False, nullable=False)
    birth_date_1 = db.Column(db.String(120), unique=False, nullable=False)
    name_2 = db.Column(db.String(120), unique=False, nullable=False)
    gender_2 = db.Column(db.String(120), unique=False, nullable=False)
    birth_date_2 = db.Column(db.String(120), unique=False, nullable=False)

    def json(self):
        return {
          'policy_key': self.policy_key,
          'number': self.number,
          'data_provider_code': self.data_provider_code,
          'data_provider_description': self.data_provider_description,
          'effective_date': self.effective_date,
          'issue_date': self.issue_date,
          'maturity_date': self.maturity_date,
          'origination_death_benefit': self.origination_death_benefit,
          'carrier_name': self.carrier_name,
          'name_1': self.name_1,
          'gender_1': self.gender_1,
          'birth_date_1': self.birth_date_1,
          'name_2': self.name_2,
          'gender_2': self.gender_2,
          'birth_date_2': self.birth_date_2
        }

with app.app_context():
    db.create_all()

# get a policy
@app.route('/policy-info/<string:number>', methods=['GET'])
def get_policy(number):
  '''
  /policy-info: given a policy number, return the
    - effective_date
    - issue_date
    - maturity_date
    - death_benefit
    - carrier_name
  '''

  try:
    policy = Policy.query.filter_by(number=number).first()
    if policy:
      payload = policy.json()
      return make_response(jsonify(
        {
          payload['number']: {
            'effective_date': payload['effective_date'],
            'issue_date': payload['issue_date'],
            'maturity_date': payload['maturity_date'],
            'death_benefit': payload['origination_death_benefit'],
            'carrier_name': payload['carrier_name']
          }
        }
      ), 200)
    return make_response(jsonify({'message': 'policy not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error getting policy'}), 500)

# get policy count
@app.route('/carrier-policy-count/<string:carrier_name>', methods=['GET'])
def get_policy_count(carrier_name):
  '''
  /carrier-policy-count: given a carrier name, return the count of all unique
  policies we have from that carrier in our database
  '''

  try:
    total = Policy.query.filter_by(carrier_name=carrier_name).count()
    if total:
      return make_response(jsonify(
        {
          carrier_name: {'unique_policies': total}
        }
      ), 200)
    return make_response(jsonify({'message': 'policy not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error getting policy'}), 500)

# get person policies
@app.route('/person-policies/<string:name>', methods=['GET'])
def get_person_policies(name):
  '''
  given a person name, return a list of all policies for that
  person regardless the position (primary or secondary) of the person on the
  policy
  '''

  try:
      primary_policies = Policy.query.filter_by(name_1=name).all()
      secondary_policies = Policy.query.filter_by(name_2=name).all()
      all_policies = []
      if primary_policies:
          for policy in primary_policies:
              all_policies.append(policy.json())

      if secondary_policies:
          for policy in secondary_policies:
              all_policies.append(policy.json())

      if len(all_policies) > 0:
          policy_list = [policy['number'] for policy in all_policies]
          return make_response(jsonify({'policies': policy_list}), 200)
      return make_response(jsonify({'message': 'policies not found'}), 404)
  except Exception as e:
      return make_response(jsonify({'error message': e}), 500)

# get data provider policies
@app.route('/data-provider-policies/<string:data_provider>', methods=['GET'])
def get_data_provider_policies(data_provider):
  '''
  given a data provider code, return the count of all
  policies that we have information on from that data provider
  '''

  try:
      total = Policy.query.filter_by(data_provider_code=data_provider).count()
      if total:
          return make_response(jsonify(
              {
                  data_provider: {'unique_policies': total}
              }
          ), 200)
      return make_response(jsonify({'message': 'policy not found'}), 404)
  except:
      return make_response(jsonify({'message': 'error getting policy'}), 500)

if __name__ == '__main__':
    app.run()
