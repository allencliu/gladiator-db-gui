# CSE385-FinalProject

## Setup Database
To set up the database for your project, follow these steps:

1. Navigate to "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
2. Open the MySQL shell with the following command:

    ```bash
    mysql --local_infile=1 -u root -p
    ```

3. Verify the local_infile setting:

    ```sql
    show global variables like 'local_infile';
    ```

4. Set global local_infile to true:

    ```sql
    set global local_infile=true;
    ```

5. Create the `gladiator` schema/database:

    ```sql
    create database gladiator;
    ```

6. Use the `gladiator` database:

    ```sql
    use gladiator;
    ```

7. Load data from the CSV file into the `gladiators` table:

    ```sql
    load data local infile
    "C:/College/Senior Year/Fall Term/CSE385/cse385-finalproject/gladiator_data.csv" into table
    gladiators
    fields terminated by ','
    optionally enclosed by '"'
    lines terminated by '\n'
    ignore 1 rows;
    ```

## Running Initial SQL

Now, run the initial SQL script to create the `gladiators` table. Execute the following command:

```bash
mysql -u root -p gladiator < initial.sql
