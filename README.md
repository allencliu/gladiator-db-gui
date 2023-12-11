# CSE385-FinalProject

## Prerequisites

### Setup Database
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

7. Running Initial SQL

    - Run the initial SQL script to create the `gladiators` table. Execute the following command in another Command Prompt window:

    ```bash
    mysql -u root -p gladiator < path/to/initial.sql
    ```

8. Load data from the CSV file from `filepath:/gladiator_data.csv` into the `gladiators` table:

    ```sql
    load data local infile
    "path/to/gladiator_data.csv" into table
    gladiators
    fields terminated by ','
    optionally enclosed by '"'
    lines terminated by '\n'
    ignore 1 rows;
    ```

9. Run the additional SQL script in the other Command Prompt window:
    ```bash
    mysql -u root -p gladiator < path/to/creategladiatortables.sql
    ```

# Gladiator Index Application

**Instructions for Running the Application**

## Prerequisites
1. Make sure you have Python installed on your system.
2. Install the required packages using the following command:
    ```pip install -r requirements.txt```

## Configuration
1. Ensure you have a MySQL server installed and running.
~~
    2. Update the database connection details in the code:
    - Host: "localhost"
    - User: "root"
    - Password: `password`
    - Database: "gladiator"
~~

## Usage Instructions

### 1. Run the Executable
- Locate the `app.exe` file in the `dist` folder.
- Double-click on `app.exe` to run the application.
~~
    - Optional: The executable may be broken after configuring, so you may need to run `app.py` instead after reconfiguring the connection details.
~~
- Make sure your database is running on localhost and your schema/database is correct i.e. gladiator
- Login with your username and password
    - Default username is `root`

### 2. Create a New Profile
- Click on the "Create Profile" button.
- In the popup window, select the tables you want to include in the profile by checking the checkboxes.
- Enter a unique profile name.
- Click the "Save" button.

### 3. Delete a Profile
- Select the profile you want to delete from the dropdown menu.
- Click the "Delete Profile" button.
- Confirm the deletion.

### 4. Search
- Enter a search query in the "Search" entry.
- Click the "Search" button to find matching records across all tables.

### 5. Navigate Through Pages
- Use the "Next" and "Previous" buttons to navigate between pages of data.
- Enter a page number in the "Go to Page" entry and click the "Go" button to jump to a specific page.

### 6. Change View
- Use the dropdown menu to select different views, such as "Gladiator Info," "Combat Stats," etc.

### 7. Sorting
- Click on the columns in the table to toggle between ascending and descending order.

# References
"Chapter&nbsp;1&nbsp;Introduction to MySQL Connector/Python." MySQL, dev.mysql.com/doc/connector-python/en/connector-python-introduction.html. Accessed 10 Dec. 2023. 
Therrien, Anthony. “Gladiator Combat Records and Profiles Dataset." Kaggle, 25 Nov. 2023, www.kaggle.com/datasets/anthonytherrien/gladiator-combat-records-and-profiles-dataset. 
"Tkinter - Python Interface to TCL/TK." Python Documentation, docs.python.org/3/library/tkinter.html. Accessed 10 Dec. 2023. 