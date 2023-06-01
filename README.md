# Preston Ventures Exercise

## Prerequisites
- [Install Docker Desktop](https://docs.docker.com/desktop/)
- [Install Python 3](https://www.python.org/downloads/)

## Step by step
This repo assumes that you are running on Mac OS. If you are running on Windows, you will need to run the `Makefile` comands manually
1. Clone this repo `git clone git@github.com:pohek321/preston-ventures-exercise.git && cd preston-ventures-exercise`
2. Ensure Docker Desktop is running and run `make init` this will complete the following:
   - Create a postgres database in docker
   - Create a flask app in docker
   - Initialize a python virtual environment
   - Install dbt adapter to that virtual environment
3. After completing step 2, run `make dbt` which will complete the following:
   - Execute a `dbt seed` to load the provided `.csv` into the docker postgres database
   - Execute a `dbt run` to execute the transformative SQL in the `/models` directory of the dbt project
   - Execute a `dbt test` to execute data quality checks against the materialized SQL
4. After completing step 3, you should be able to navigate to some URL's to see the API endpoints in action:
   - [policy-info](http://localhost:4000/policy-info/USTXQOE)
   - [carrier-policy-count](http://localhost:4000/carrier-policy-count/AXA%20Equitable)
   - [person-policies](http://localhost:4000/person-policies/Rebecca%20Wagnon)
   - [data-provider-policies](http://localhost:4000/data-provider-policies/GRT)
5. When you are finished with the application, you can run `docker kill $(docker ps -q)` to kill the docker containers