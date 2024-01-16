# Database Connection Library

This library provides two classes, `ACCESSdbc` and `SSMSdbc`, for connecting to Microsoft Access and SQL Server databases respectively.

## Installation

```bash 
pip install db_handler
```

## Usage
## Connecting to a Microsoft Access Database
```bash 
from db_handler import ACCESSdbc

# Create an instance of ACCESSdbc
db = ACCESSdbc('path_to_your_database_file')

# Connect to the database
if db.connect():
    # Execute a query and get the results
    results = db.execute_query_return_results('SELECT * FROM your_table')

    # Don't forget to disconnect when you're done
    db.disconnect()
```
## Connecting to a Microsoft SQL Server Database
```bash 
from db_handler import SSMSdbc

# Create an instance of SSMSdbc
db = SSMSdbc('your_server', 'your_database', 'your_username', 'your_password')

# Connect to the database
if db.connect():
    # Execute a query and get the results
    results = db.execute_query_return_results('SELECT * FROM your_table')

    # Don't forget to disconnect when you're done
    db.disconnect()
```

