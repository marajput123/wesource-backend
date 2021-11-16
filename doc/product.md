# Product REST Endpoints

### GET Endpoint

_Get a single product with the provided id_

```
GET http://127.0.0.1:5000/api/product/<product_id>
```
#### URI Parameters
| Name       | In       | Type     | Description |
| -------    | ------   | -------- | --------- |
| product_id | param    | string   | Id of the the product |


### POST Endpoint

_Post a single product_

```
POST http://127.0.0.1:5000/api/product
```
#### __BODY Parameters__

| Name       | In       | Type     | Description | Required
| -------    | ------   | -------- | --------- | -------|
| title      | body     | string   | Product title | True
| description| body     | string   | Description | True
| quantity   | body     | int or string | Quantity of the product| True
| items      | body     | Product Item   | Embedded product item objects | True

#### __Product Item__

|Name       | In        | Type      | Description | Required |
| ------- | ------    | --------  | -------------   | -------- |
| title     | items | string | Title of the embedded product item | True |
| description | items | string |  Description of the embeded product item | True |
| price | items | int | Price of the embedded product item | True
| quantity | items | int | Price of the embedded product item | True


### PUT Endpoint

_Update the specified product_

```
PUT http://127.0.0.1:5000/api/product/<product_id>
```
#### __URI Parameters__
| Name       | In       | Type     | Description |
| -------    | ------   | -------- | --------- |
| product_id | param    | string   | Id of the the product |

#### __BODY Parameters__
| Name       | In       | Type     | Description | Rquired |
| -------    | ------   | -------- | --------- | ------- |
| title      | body     | string   | Product title | False
| description| body     | string   | Description | False
| quantity   | body     | int or string | Quantity of the product| False


### DELETE Endpoint

_Delete the specified product_

```
DELETE http://127.0.0.1:5000/api/product/<product_id>
```
#### URI Parameters
| Name       | In       | Type     | Description |
| -------    | ------   | -------- | --------- |
| product_id | param    | string   | Id of the the product |


### GET ALL Products

_Get all products with the given query_

```
GET http://127.0.0.1:5000/api/products/<?queries>
```
#### URI Queries
| Name       | In       | Type     | Description |
| -------    | ------   | -------- | --------- |
| title | query | string   | title of the product |
| price__lte | query | string | price less than | 
| price__gte | query | string | price greater than |
| quantity__lte | query | string | quantity less than | 
| quantity__gte | query | string | quantity greater than |
| date__lte | query | string | date less than | 
| date__gte | query | string | date greater than |
| page | query | string | page number |


