# REST API
Starting `>4.3.1`, REST API support is added in an experimental manner. These APIs will be backed by [Django Rest Framework](https://www.django-rest-framework.org/) with authentication token support. 

APIs that follow this convention should be denoted by `api/v2/` prefix. 

## Token Authentication
REST APIs will use token authentication.

### Generating a Token
Currently, only manual generation of tokens is supported. 

```
python3 manage.py shell_plus
from rest_framework.authtoken.models import Token
token = Token.objects.create(user=...)
```

### Authorization
Include the following header in all API calls.

```
Authorization: Token <API TOKEN>
```

## Future Plans
Eventually, all endpoints should be REST backed to enable UI frameworks like Vue.js, instead of server-side generated templates. 