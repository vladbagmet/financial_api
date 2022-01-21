# Financial API Backend
Implements backend for managing financial accounts and funds.
Financial accounts can be created and owned and managed by their owners.
DISCLAIMER. On the repository there is a file `.env`. It was added to make project local start easier. It should be removed in production.


## Prerequisites
* Unix-like OS (like MacOs or Linux)
* Docker-compose (if you do not have one, feel fre to get installation package here https://docs.docker.com/desktop/mac/install/)


## Running Service Locally
Use terminal to run commands below
* Clone repository by running `git clone https://github.com/vladbagmet/financial_api.git`
* Go to the cloned repository by running `cd financial_api`
* Run service by executing a shortcut command `make start`
Service runs inside docker-container and can accept HTTP requests on `http://127.0.0.1:8000` address.


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


### Transfer Funds

### Retrieve Transfers History
