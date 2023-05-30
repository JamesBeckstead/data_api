// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table data_providers {
  provider_id integer [primary key]
  name varchar
  code varchar
  priorty int
}

Table benefits {
  benefit_id integer [primary key]
  death_benefit int
}

Table policies {
  policy_id integer [primary key]
  benefit_id integer
  carrier_id integer
  insured_id integer
  provider_id integer
  effective_date integer
  issue_date integer
  maturity_date integer
  created_at timestamp
}

Table carriers {
  carrier_id integer [primary key]
  name varchar
}

Table insured {
  insured_id integer [primary key]
  dob_date integer
  insured_name varchar
}

Table dates {
  date_id integer [primary key]
  date_value date
}
Ref: dates.date_id < policies.maturity_date

Ref: dates.date_id < policies.issue_date

Ref: dates.date_id < policies.effective_date

Ref: insured.insured_id < policies.insured_id

Ref: carriers.carrier_id < policies.carrier_id

Ref: benefits.benefit_id < policies.benefit_id

Ref: data_providers.provider_id < policies.provider_id