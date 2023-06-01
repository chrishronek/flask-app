with priority_1 as (
  select
    *
  from (
    select
      md5(name_1 || issue_date) as policy_key,
      *,
      row_number() over (partition by md5(name_1 || issue_date) order by issue_date desc) as rn
    from {{ ref('life_policy_data') }}
    where data_provider_priority = 1
  ) p1_hashed
  where p1_hashed.rn = 1
),

priority_2 as (
  select
    *
  from (
    select
      md5(name_1 || issue_date) as policy_key,
      *,
      row_number() over (partition by md5(name_1 || issue_date) order by issue_date desc) as rn
    from {{ ref('life_policy_data') }}
    where data_provider_priority = 2
  ) p1_hashed
  where p1_hashed.rn = 1
),

priority_3 as (
  select
    *
  from (
    select
      md5(name_1 || issue_date) as policy_key,
      *,
      row_number() over (partition by md5(name_1 || issue_date) order by issue_date desc) as rn
    from {{ ref('life_policy_data') }}
    where data_provider_priority = 3
  ) p1_hashed
  where p1_hashed.rn = 1
),

policy_keys as (
  select
    policy_key
  from priority_1

  union

  select
    policy_key
  from priority_2

  union

  select
    policy_key
  from priority_3
)

select
  policy_keys.policy_key,
  coalesce(priority_1.number, priority_2.number, priority_3.number) as number,
  coalesce(priority_1.data_provider_code, priority_2.data_provider_code, priority_3.data_provider_code) as data_provider_code,
  coalesce(priority_1.data_provider_description, priority_2.data_provider_description, priority_3.data_provider_description) as data_provider_description,
  coalesce(priority_1.effective_date, priority_2.effective_date, priority_3.effective_date) as effective_date,
  coalesce(priority_1.issue_date, priority_2.issue_date, priority_3.issue_date) as issue_date,
  coalesce(priority_1.maturity_date, priority_2.maturity_date, priority_3.maturity_date) as maturity_date,
  coalesce(priority_1.origination_death_benefit, priority_2.origination_death_benefit, priority_3.origination_death_benefit) as origination_death_benefit,
  coalesce(priority_1.carrier_name, priority_2.carrier_name, priority_3.carrier_name) as carrier_name,
  coalesce(priority_1.name_1, priority_2.name_1, priority_3.name_1) as name_1,
  coalesce(priority_1.gender_1, priority_2.gender_1, priority_3.gender_1) as gender_1,
  coalesce(priority_1.birth_date_1, priority_2.birth_date_1, priority_3.birth_date_1) as birth_date_1,
  coalesce(priority_1.name_2, priority_2.name_2, priority_3.name_2) as name_2,
  coalesce(priority_1.gender_2, priority_2.gender_2, priority_3.gender_2) as gender_2,
  coalesce(priority_1.birth_date_2, priority_2.birth_date_2, priority_3.birth_date_2) as birth_date_2
from policy_keys
left join priority_1 on priority_1.policy_key = policy_keys.policy_key
left join priority_2 on priority_2.policy_key = policy_keys.policy_key
left join priority_3 on priority_3.policy_key = policy_keys.policy_key
where policy_keys.policy_key is not null