# Hivery
Paranuara Challenge

## Prerequisites
- virtualenv
If not installed install it using
```
pip install virtualenv 
```

- MySQL setup


## Setup
- Create a pull of the current github project.
- Open a terminal and navigate to the project folder and initate the vitual environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```
- Change the password in *'data.py'* and *'hivery/db.py'* to match the MySQL local database password
- Login to MySQL localhost and create a schema named 'hivery'

```
CREATE SCHEMA `hivery` ;
```

- To load the data from the JSON present in the resources folder execute the standalone python script as below

```
 python data.py 
 ```

## Local server(w Hot reloading)

```
gunicorn --reload hivery.app

```
This should start the server at *http://localhost*

## Test Notes
We are making use of pytest to test the falcon API created.Run the test script as follows

```
pytest test 
```



## Code Structure
```
/data.py - standalone python script which will load the data from the JSON to MySQL DB
/hivery - Falcon API
/hivery/app.py - Falcon API app
/hivery/paranuara.py - Resource to serve the API

```

## API spec

Execute the below API in any browser of your choice

- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.

``` 
http://localhost:8000/v1/company/{company_name} 
```

**Sample**
```
 http://localhost:8000/v1/company/TECHTRIX*
```

```
            {
                "employees": [
                    "Mabel Steele",
                    "Beatriz Holder",
                    "Mcleod Mcbride",
                    "Knapp Moss",
                    "Bass Hansen",
                    "Janine Hill",
                    "Alisha Blackburn"
                ]
            }
            
```

- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.

``` 
http://localhost:8000/v1/people/{ppl_one},{ppl_two} 
```

**Sample**

```
http://localhost:8000/v1/people/Cote Booth,Rena Vincent
```

```
{
    "details": [
        {
            "address": "394 Loring Avenue, Salvo, Maryland, 9396",
            "age": "26",
            "name": "Cote Booth",
            "phone": "+1 (842) 598-3525"
        },
        {
            "address": "872 Nassau Street, Harviell, Utah, 9532",
            "age": "22",
            "name": "Rena Vincent",
            "phone": "+1 (978) 575-2298"
        }
    ],
    "mutual_friends": [
        "Decker Mckenzie"
    ]
 }
   ```

- Given 1 people, provide a list of fruits and vegetables they like.

``` 
http://localhost:8000/v1/people/{ppl_one} 
```

**Sample**

```
http://localhost:8000/v1/people/Cote Booth
```


```     
        {
            "age": "26",
            "fsruits": [
                "strawberry"
            ],
            "username": "Cote Booth",
            "vegetables": [
                "beetroot",
                "carrot",
                "cucumber"
            ]
        }
   ```
