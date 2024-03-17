**Api_Refs** Api for working with user referer system. Created with DRF

# Quick start

##### Download image from docker hub

---
```
docker pull sergeynaum/users_balanse:latest
```
---
##### Start the container by running the command
```
make docker_start
```
---
##### CONGRATULATIONS THE CONTAINER IS UP AND RUNNING AND THE API IS READY FOR TESTING_🚀

---
###### В Приложении используется апи для проверки работоспособности email адреса [abstractapi.com](https://app.abstractapi.com/api/email-validation/) 
т.е. использование api от emailhunter.co доступно только при наличии корпоративного email.
---
### Available methods for API requestsAvailable methods for API requests

Swagger ui documentation
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

Output wallets of all users by GET method
```
curl http://127.0.0.1:8000/api/v1/balance/
```