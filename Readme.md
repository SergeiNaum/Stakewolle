# **Api_Refs** Api for working with user referer system. Created with DRF, Celery, redis

## Quick start


##### Download image from docker hub

---
```
docker pull sergeynaum/electroservice:latest
```
---

##### create directory app and navigate to it

```
mkdir app && cd app
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
Output wallets of all users by GET method
```
curl http://127.0.0.1:8000/api/v1/balance/
```


---
###### The Appendix uses an api to test the validity of the email address [abstractapi.com](https://app.abstractapi.com/api/email-validation/) as the api from emailhunter.co is only available if you have a corporate email.

---

###### Also I could not install the clearbit library to work with the data enrichment api clearbit.com/enrichment so I decided to write pseudo code as I would do it. This code is commented out because the clearbit library does not work with modern versions of python, and I was afraid to change the version of python in an already working project.

###### Since DRF does not support asynchrony to emit asynchrony in the project I use Celery - mechanism of deferred tasks, how well it worked out for me is for you to judge, I am always open to criticism because it is criticism that makes me a better specialist.

---