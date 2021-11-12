# AUTH Endpoint

### POST Endpoint (Login)

_Login User_

```
POST http://127.0.0.1:5000/api/login
```

#### Body Parameters
| Name | In | Type | Description | Rquired |
| ------- | ------- | ------ | ------- | ------|
| email | Body | string | email of the user | True |
| password | Body | string | password of the user| True|

### POST Endpoint (Register)

_Register User_
```
POST http://127.0.0.1:5000/api/auth/<user_id>
```

#### Body Parameters
| Name | In | Type | Description | Required |
| ------- | ------- | ------ | ------- | -------- |
| firstName | Body | String |First Name | True |
| lastname | Body | String | Last Name | True |
| username | Body | String | Username | True |
| email | Body | String | Email Address | True |
| password | Body | String | Password | True |

### PUT Endpoint

_Update the User_
```
PUT http://127.0.0.1:5000/api/auth/<user_id>
```

### Body Parameters
| Name | In | Type | Description | Required |
| ------- | ------- | ------ | ------- | -------- |
| firstName | Body | String |First Name | False |
| lastname | Body | String | Last Name | False |