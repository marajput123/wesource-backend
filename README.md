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
> db_populate_script.py cu   
```

#### 5.2 Creating Products

Create products from the ./data/products.json file

```sh
> db_populate_script.py cp   
```

#### 5.3 Creating Group

Create products from the ./data/group.json file

```sh
> db_populate_script.py cg   
```

#### 5.4 Creating Group

Create products from the ./data/review.json file

```sh
> db_populate_script.py cr   
```

#### 5.5 Creating multiple collections
Create mulitple collections from the ./data folder
```sh
# Create User collection and Product collection
> db_populateScript.py cu cp 
# Create Group collection and Review collection
> db_populateScript.py cg cr 
# Create all collections
> db_populate_script.py cu cp cg cr
```

#### 5.6 Dropping Collections

Dropping collections from the databse

```sh
# Drop User collection
> db_populateScript.py du 
# Drop Product collection 
> db_populateScript.py dp
# Drop Group collection 
> db_populateScript.py dg
# Drop Review collection 
> db_populateScript.py dr
# Drop all collections
> db_populate_script.py delete_all
```

***
*Reference -*  [Flask Installation Guide](https://flask.palletsprojects.com/en/2.0.x/installation/#create-an-environment)

*If there are errors in this .md file, please update. Thank you!*






