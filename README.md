# Dummy Financial Organisation API Backend
Implements backend for managing accounts and funds for dummy financial organisation.
Financial accounts can be created, owned and managed by their owners.
The purposes of this application are:
* to show how to set application fast
* have JWT authentication implemented
* have infrastructure for end-to-end API testing.


## Prerequisites
* Unix-like OS (like MacOs or Linux)
* Docker-compose (if you do not have one, feel fre to get installation package here https://docs.docker.com/desktop/mac/install/)


## Running Service Locally
Use terminal to run commands below
* Clone repository by running `git clone https://github.com/vladbagmet/financial_api.git`
* Go to the cloned repository by running `cd financial_api`
* Create `.env` file with database credentials or use a template file with default dev credentials by running `cp ./backend/.env.sample ./backend/.env`
* Run service by executing a shortcut command `make start`
Service runs inside docker-container and can accept HTTP requests on `http://0.0.0.0:8000/` address.


## Running Tests
* Run tests by executing a shortcut command `make test`


## Api Service Documentation
All request should contain header with `Content-Type`: `application/json`. 
Requests against endpoints with authentication should also include header with `Authorization`: `Bearer {{token}}`


### Authentication
[POST] `/api/auth/register/` | [no_auth] Used to register new users

Body Parameters
* `username`
* `password`
* `first_name` (optional)
* `last_name`(optional)


[POST] `/api/auth/login/` | [no_auth] Used to log in

Body Parameters
* `username`
* `password`


[POST] `/api/auth/login/refresh/` | [no_auth] Used to get access token by providing a refresh token

Body Parameters
* `refresh`



### Account
[POST] `/api/accounts/` | [auth] Used to create an account

Body Parameters
* `name` Name of an account that will be created
* `balance` (optional) Initial balance for newly-created account, if not specified, 0.0 will be set
* `currency` (optional) Currency for newly-created account, if not specified, "USD" will be set
  * possible options ['USD']


[GET] `/api/accounts/<uuid4:account_id>/` | [auth] Used to retrieve account balance


[POST] `/api/accounts/<uuid4:account_id>/transfer/<uuid4:account_id>/` [auth] Used to transfer funds between 2 different accounts

Body Parameters
* `amount` Decimal positive number to transfer
* `currency` Indicates the currency of the transaction, for now only "USD" transfers are allowed



### Transfers History
[GET] `/api/transfers_history/<uuid4:account_id>/` | [auth] Used for retrieve transfers history for the given account



## Demos
### Log In
![fin-demo-login](https://user-images.githubusercontent.com/23407924/150554363-59622d11-c990-4f6a-ae90-053533c0a92b.gif)


### Create Account
![fin-demo-account-creation](https://user-images.githubusercontent.com/23407924/150556107-98ccc01b-5c13-4293-9c4b-4ed394a71247.gif)


### Retrieve Balance
![fin-demo-retrieve-balance](https://user-images.githubusercontent.com/23407924/150557979-57199e31-d66d-49c6-ad7d-3a861f334c9e.gif)


### Funds Transfers
![fin-demo-funds-transfers](https://user-images.githubusercontent.com/23407924/150559075-edfe24f5-748d-4aac-85d9-1e54833f90e8.gif)


### Retrieve Transfers History
![fin-demo-transfers-history](https://user-images.githubusercontent.com/23407924/150560008-ae83e26a-81e9-48c3-99c4-8891581c67a7.gif)
