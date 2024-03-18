[![Lint Code](https://github.com/SergeiNaum/Stakewolle/actions/workflows/linter_check.yml/badge.svg)](https://github.com/SergeiNaum/Stakewolle/actions/workflows/linter_check.yml)
# Test task for the company Stakewolle
# **Api_Refs** Api for working with user referer system. Created with DRF, Celery, redis


## Quick start

### For your convenience, the application is deployed on my private server at:
#### --> [CLICK FOR TEST HERE](http://77.222.53.154:8000/api/schema/swagger-ui/) <--
  
#### Or you can deploy the project locally by following these instructions:

##### clonne project from repo

```
git clone https://github.com/SergeiNaum/Stakewolle.git
```
---

##### navigate to project_folder

```
cd Stakewolle
```
---

##### Start app execute the command
```
docker-compose up
```
---
##### CONGRATULATIONS THE CONTAINER IS UP AND RUNNING AND THE API IS READY FOR TESTING_🚀

---

##### Available methods for API requestsAvailable methods for API requests

Swagger ui documentation
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```
---
Or use curl or Postman


Generate jwt tokens (access and refresh)
```
curl http://127.0.0.1:8000/api/token/
```

---

Update jwt token upon entry refresh token
```
curl http://127.0.0.1:8000/api/token/refresh/
```

---

Takes a token and indicates if it is valid. This view provides no information about a token's fitness for a particular use.
```
curl http://127.0.0.1:8000/api/token/verify/
```
---

Create a new referral code for the user
```
curl -X POST http://127.0.0.1:8000/referral-code/
```

Destroy a user's referral code
```
curl -X DELETE http://127.0.0.1:8000/referral-code/delete/
```

---

Show referal code for authenticated user but 
```
curl http://127.0.0.1:8000/referral-codes/<uuid:task_id>/result/
```

---

Retrieve a referral code by email
```
curl -X POST http://127.0.0.1:8000/referral-code/by-email/ -d '{"email": "example@example.com"}' -H "Content-Type: application/json"
```

Show all referrals for current is authenticated user
```
curl http://127.0.0.1:8000/referrals/
```

---

Registration new user by username, password, password2, email
```
curl -X POST http://127.0.0.1:8000/register/ -d '{"username": "jks3WBi_L2_ta0KgCD9yn@wUZBbeNEI", "password": "string", "password2": "string", "email": "user@example.com"}' -H "Content-Type: application/json"
```

---

Registration new referer user by username, password, email, referral_code
```
curl -X POST http://127.0.0.1:8000/register/refer/ -d '{"username": "SZjGbYbxb", "email": "user@example.com", "password": "string", "referral_code": "string"}' -H "Content-Type: application/json"
```

---

**To stop app, execute the command**

```
docker-compose down -v
```


---
###### The Appendix uses an api to test the validity of the email address [abstractapi.com](https://app.abstractapi.com/api/email-validation/) as the api from emailhunter.co is only available if you have a corporate email.

---

###### Also I could not install the clearbit library to work with the data enrichment api clearbit.com/enrichment so I decided to write pseudo code as I would do it. This code is commented out because the clearbit library does not work with modern versions of python, and I was afraid to change the version of python in an already working project.

###### Since DRF does not support asynchrony to emit asynchrony in the project I use Celery - mechanism of deferred tasks, how well it worked out for me is for you to judge, I am always open to criticism because it is criticism that makes me a better specialist.

---

