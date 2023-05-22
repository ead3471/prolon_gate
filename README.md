# Prolon Gate project

ProlonGate is a module designed for requesting and auto load data from Prolon controllers via Modbus RTU protocol to the remote MySql database.
***
## Features

- Read data from Prolon controlelrs
- Store data in the local sqlite database
- Synchronize local database with remote MySQL database
- Read/Write each connected device data manually via http requests
- Read/Write each connected device data from remote server through database table

## Installation
1. Download install Python 2.7
2. Clone project from Github
   ```
   git clone git@github.com:ead3471/prolon_gate.git
   ```
3. Navigate to the cloned folder 
   ```
   cd prolon_gate
   ```
4. Init and activate virtual environment with python 2.7
   ```
   virtualenv -p `which python2.7` venv
   ```
5. Install dependencies
   ```
   pip install -r requirements.txt
   ```
6. Create folders for loggers
    ```
   mkdir -p logs/server
   mkdir -p logs/sync
   mkdir -p logs/db_requests
   ```

7. Create tables in remote database(see resources/remote_tables_create.txt)
8. Create file resources/meter_data.sqlite
9. Create tables in local database(see resources/local_tables_create.txt)
10. Start all tasks with run_all.cmd file
