# **WeSource Backend**

## Section 1 - Environment Setup

### 1. Creating the directories

```sh
> mkdir capstone 
> cd capstone
```

### 2. Creating Virtual Enivornment 

```sh
# inside the ./capstone directory
> py -m venv venv
> venv\Scripts\activate
```

*Note -* The ```py -m venv venv``` command may be different for you. It could be ```py -3 -m venv venv``` **or** ```python -m venv venv```

### 3. Cloning the Git Repo
```sh
# inside the ./capstone directory
> git init
> git clone https://github.com/marajput123/WeSource-backend.git
```

### 4. Installing dependencies 
```sh
> pip install -r requirements.txt 
```

### 5. Populating Database

*Note -* Be under the root directory (./WeSource-backend)

#### 5.1 Creating Users

Create users from the ./data/users.json file

```sh
> db_populateScript.py cu   
```

#### 5.2 Creating Products

Create products from the ./data/products.json file

```sh
> db_populateScript.py cp   
```

#### 5.4 Creating multiple collections
Create mulitple collections from the ./data folder
```sh
# Create User collection and Product collection
> db_populateScript.py cu cp 
# Create all collections
> db_populateScript.py cu cp
```

#### 5.5 Dropping Collections

Dropping collections from the databse

```sh
# Drop User collection
> db_populateScript.py du 
# Drop Product collection 
> db_populateScript.py dp
# Drop all collections
> db_populateScript.py delete_all
```

***
*Reference -*  [Flask Installation Guide](https://flask.palletsprojects.com/en/2.0.x/installation/#create-an-environment)

*If there are errors in this .md file, please update. Thank you!*






