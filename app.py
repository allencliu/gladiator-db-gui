import mysql.connector
import tkinter as tk
from tkinter import ttk

host = "localhost"
user = "root"
password = "&%Bn96=mdQe4"
database = "gladiator"

# Global variable for pagination
current_offset = 0

sort_column = None
sort_order = "ASC"

# Function to create a new profile with selected tables
def create_profile():
    # Create a new window for profile creation
    create_profile_window = tk.Toplevel(root)
    create_profile_window.title("Create New Profile")

    # Create a dictionary to store checkbox variables
    checkbox_vars = {}

    def get_column_type(table, column):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="&%Bn96=mdQe4",
            database="gladiator"
        )

        cursor = connection.cursor()

        # Query the information_schema to get column information
        cursor.execute("""
            SELECT COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
        """, (connection.database, table, column))

        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            # Default to VARCHAR if the column type is not found
            return "VARCHAR(255)"
    
    def generate_create_table_query(profile_name):
        ## Get the profile name
        selected_tables = [table for table, var in checkbox_vars.items() if var.get()]

        if not selected_tables:
            print("Please select at least one table.")
            return

        # Create a table name based on selected tables
        

        # Start building the CREATE TABLE statement
        query = f"CREATE TABLE {profile_name} (\n"

        # Add auto-incrementing primary key column
        query += "GladiatorID INT AUTO_INCREMENT,\n"
        # Add columns for the first selected table
        columns = [f"{col} {get_column_type(selected_tables[0], col)}" for col in get_columns(selected_tables[0])]

        for i in range(1, len(selected_tables)):
        # Add columns for the subsequent tables (excluding GladiatorID)
            columns.extend([f"{col} {get_column_type(selected_tables[i], col)}" for col in get_columns(selected_tables[i]) if col != "GladiatorID"])

        # Join columns into a single string
        query += ",\n".join(columns)

        # Add primary key constraint
        query += f",\nPRIMARY KEY (GladiatorID)"

        # Close the CREATE TABLE statement
        query += "\n);"

        return query

    def generate_insert_query(profile_name):
        query = f"INSERT INTO {profile_name} ("

        selected_tables = [table for table, var in checkbox_vars.items() if var.get()]

        if not selected_tables:
            print("Please select at least one table.")
            return

        # Add columns for the first selected table
        columns = ["GladiatorID"]
        columns.extend([f"{col}" for col in get_columns(selected_tables[0])])

        for i in range(1, len(selected_tables)):
            # Add columns for the subsequent tables (excluding GladiatorID)
            columns.extend([f"{col}" for col in get_columns(selected_tables[i]) if col != "GladiatorID"])

        # Join columns into a single string
        query += ", ".join(columns)

        # Close column names and open the SELECT statement
        query += ") SELECT "

        # Add GladiatorID column for the first selected table
        query += f"{selected_tables[0]}.GladiatorID, "

        # Add other columns for the first selected table
        query += ", ".join([f"{selected_tables[0]}.{col}" for col in get_columns(selected_tables[0])])
        for i in range(1, len(selected_tables)):
            # Add other columns for the subsequent tables (excluding GladiatorID)
            query += ", " + ", ".join([f"{selected_tables[i]}.{col}" for col in get_columns(selected_tables[i]) if col != "GladiatorID"])
        
        # Add FROM clause
        query += f" FROM {selected_tables[0]}"

        # Join subsequent tables using the specified condition
        for i in range(1, len(selected_tables)):
            # Add JOIN condition
            query += f" JOIN {selected_tables[i]} ON {selected_tables[i-1]}.GladiatorID = {selected_tables[i]}.GladiatorID"

        # Close the SELECT statement
        query += ";"

        return query


        
    # Function to get the selected tables and create the profile
    def save_profile():
        # query = generate_query()
        ## Get the profile name
        profile_name = name_entry.get().strip()  # Strip leading and trailing whitespaces
        # Check if the profile name is empty
        if not profile_name:
            print("Error: Profile name cannot be blank.")
            return

        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            if connection.is_connected():
                mycursor = connection.cursor()
                # Insert the new profile into the Profiles table
                insert_query = "INSERT INTO Profiles (ProfileName) VALUES (%s);"
                data = (profile_name,)
                # print(f"Executing query: {insert_query}")
                # print(f"Data: {data}")
                mycursor.execute(insert_query, data)
                connection.commit()

                
                # Step 1: Generate and execute the CREATE TABLE query
                create_table_query = generate_create_table_query(profile_name)
                print(create_table_query)  # Print the query for debugging
                mycursor.execute(create_table_query)
                
                # Step 2: Generate and execute the INSERT INTO query
                insert_query = generate_insert_query(profile_name)
                print(insert_query)  # Print the query for debugging
                mycursor.execute(insert_query)
                # Commit the changes
                connection.commit()
                # print(result)
                # Fetch all columns from the table associated with the profile_name
                query = f"SELECT * FROM gladiator.{profile_name};"
                mycursor.execute(query)
                result = mycursor.fetchall()
                # Display the selected data in the Treeview
                tree.delete(*tree.get_children())  # Clear existing data
                columns = [desc[0] for desc in mycursor.description]
                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)  # Adjust the width as needed

                for row in result:
                    tree.insert("", "end", values=row)

                connection.commit()
                
                # Update the dropdown menu with the new profile
                profiles.append(profile_name)  # Assuming the profile name is unique
                profile_dropdown['values'] = profiles
                profile_dropdown.set(profile_name)  # Set the new profile as selected

                # Update the dropdown with created profiles
                profile_dropdown['values'] = profiles

                # Close the profile creation window
                create_profile_window.destroy()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print("Connection closed")

    # Create checkboxes for each table, including GladiatorInfo
    for table in ["GladiatorInfo", "CombatStats", "Skills", "BackgroundInfo", "HealthInfo", "ExternalFactors", "Outcome"]:
        var = tk.IntVar()
        checkbox_vars[table] = var
        checkbox = tk.Checkbutton(create_profile_window, text=table, variable=var)
        checkbox.pack()

    # Create labels and entry widgets for profile details
    name_label = tk.Label(create_profile_window, text="Profile Name:")
    name_label.pack()
    name_entry = tk.Entry(create_profile_window)
    name_entry.pack()

    # Button to save the new profile
    save_button = tk.Button(create_profile_window, text="Save", command=save_profile)
    save_button.pack()




# Function to fetch data for a specific tree with pagination and sorting
def fetch_data_for_tree(tree_option):
    global current_offset

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connected to MySQL Server")

            mycursor = connection.cursor()

            # Fetch all records for the current page
            query = f"SELECT * FROM gladiator.{tree_option.replace(' ', '').lower()} LIMIT {limit} OFFSET {current_offset};"
            mycursor.execute(query)
            result = mycursor.fetchall()

            # Sort the records within Python
            if sort_column and sort_column in get_columns_for_tree(tree_option):
                result.sort(key=lambda x: x[get_columns_for_tree(tree_option).index(sort_column)], reverse=(sort_order == "DESC"))

            # Clear existing data in the Treeview
            for row in tree.get_children():
                tree.delete(row)

            # Set column headings
            columns = get_columns_for_tree(tree_option)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col, command=lambda c=col: sort_tree(tree, tree_option, c))
                tree.column(col, width=100)  # Adjust the width as needed

            # Insert new data into the Treeview
            for row in result:
                tree.insert("", "end", values=row)

            # Update the current page label
            update_current_page_label()


    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

# Function to update the current page label
def update_current_page_label():
    global current_offset
    current_page = current_offset // limit + 1
    current_page_label.config(text=f"Page: {current_page}")


# Function to get table name from a column name
def get_table_name(column):
    if column:
        for table_option in tree_options:
            if column in get_columns_for_tree(table_option):
                return table_option
    return None

# Function to sort the Treeview
def sort_tree(tree, tree_option, column):
    global sort_column, sort_order, current_offset
    # Determine the current sort order for the column
    if sort_column == column:
        sort_order = "DESC" if sort_order == "ASC" else "ASC"
    else:
        sort_column = column
        sort_order = "ASC"

    # Fetch data for the current page
    fetch_data_for_tree(tree_option)

# Update event handlers for "Next" and "Previous" buttons
def on_next():
    global current_offset
    current_offset += limit
    fetch_data_for_tree(selected_option)

def on_previous():
    global current_offset
    current_offset = max(0, current_offset - limit)
    fetch_data_for_tree(selected_option)


# Update event handler for "Go to Page" entry
def on_go_to_page():
    try:
        page_number = int(go_to_page_entry.get())
        global current_offset
        current_offset = max(0, (page_number - 1) * limit)
        fetch_data_for_tree(selected_option)
        go_to_page_entry.delete(0, tk.END)
    except ValueError:
        print("Invalid page number")

# Function to get columns for a specific tree
def get_columns_for_tree(tree_option):
    # Define your columns for each tree
    if tree_option == "Gladiator Info":
        return ("GladiatorID", "Name", "Age", "BirthYear", "Origin", "Height", "Weight")
    elif tree_option == "Combat Stats":
        return ("GladiatorID", "Category", "Wins", "Losses")
    elif tree_option == "Skills":
        return ("GladiatorID", "SpecialSkills", "WeaponOfChoice", "BattleStrategy", "CrowdAppealTechniques", "TacticalKnowledge")
    elif tree_option == "Background Info":
        return ("GladiatorID", "PreviousOccupation", "TrainingIntensity", "BattleExperience", "PersonalMotivation", "AllegianceNetwork")
    elif tree_option == "Health Info":
        return ("GladiatorID", "InjuryHistory", "MentalResilience", "DietAndNutrition", "PsychologicalProfile", "HealthStatus")
    elif tree_option == "External Factors":
        return ("GladiatorID", "EquipmentQuality", "PatronWealth", "PublicFavor", "SocialStanding")
    elif tree_option == "Outcome":
        return ("GladiatorID", "Survived")
    
def get_columns(table):
    if table == "GladiatorInfo":
        return ("Name", "Age", "BirthYear", "Origin", "Height", "Weight")
    elif table == "CombatStats":
        return ("Category", "Wins", "Losses")
    elif table == "Skills":
        return ("SpecialSkills", "WeaponOfChoice", "BattleStrategy", "CrowdAppealTechniques", "TacticalKnowledge")
    elif table == "BackgroundInfo":
        return ("PreviousOccupation", "TrainingIntensity", "BattleExperience", "PersonalMotivation", "AllegianceNetwork")
    elif table == "HealthInfo":
        return ("InjuryHistory", "MentalResilience", "DietAndNutrition", "PsychologicalProfile", "HealthStatus")
    elif table == "ExternalFactors":
        return ("EquipmentQuality", "PatronWealth", "PublicFavor", "SocialStanding")
    elif table == "Outcome":
        return ("Survived",)

def fetch_profile_data(profile_name, sort_column=None, sort_order="ASC"):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connected to MySQL Server")

            mycursor = connection.cursor()

            # Formulate the SELECT * query
            query = f"SELECT * FROM gladiator.{profile_name};"
            mycursor.execute(query)
            result_data = mycursor.fetchall()

            # Clear existing data in the Treeview
            for row in tree.get_children():
                tree.delete(row)

            # Set column headings
            columns = [desc[0] for desc in mycursor.description]
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col, command=lambda c=col: sort_tree(tree, profile_name, c))
                tree.column(col, width=100)  # Adjust the width as needed

            # Sort the records within Python
            if sort_column and sort_column in columns:
                result_data.sort(key=lambda x: x[columns.index(sort_column)], reverse=(sort_order == "DESC"))

            # Insert new data into the Treeview
            for row in result_data:
                tree.insert("", "end", values=row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

def fetch_profile_names():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Connected to MySQL Server")

            mycursor = connection.cursor()
            create_profile_table_query = "CREATE TABLE IF NOT EXISTS Profiles (ProfileName VARCHAR(24) PRIMARY KEY);"
            mycursor.execute(create_profile_table_query)
            connection.commit()
            # Fetch profile names from the Profiles table
            query = "SELECT ProfileName FROM Profiles;"
            mycursor.execute(query)
            result = mycursor.fetchall()

            # Extract profile names from the result
            profile_names = [row[0] for row in result]

            # Update the profile dropdown with profile names
            profile_dropdown['values'] = profile_names

            # Optionally, select the first profile and fetch data for it
            if profile_names:
                selected_profile = profile_names[0]
                fetch_profile_data(selected_profile)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")
            
# Create the main Tkinter window
root = tk.Tk()
root.title("Gladiator Index")

root.geometry("1600x900")

# Create a Treeview widget to display data
columns = ("GladiatorID", "Name", "Age", "BirthYear", "Origin", "Height", "Weight")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Set up column headings with sorting capability
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: sort_tree(tree, selected_option, c))
    tree.column(col, width=100)  # Adjust the width as needed

# Configure the style for the Treeview widget
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))  # Adjust the font family and size
style.configure("Treeview.Heading", font=("Arial", 12))

# Dropdown menu and fetch button nav_container
nav_container = ttk.Frame(root)

filter_container = ttk.Frame(root)

# Profile list
profiles = []

# Create a dropdown for selecting profiles
profile_dropdown_label = tk.Label(filter_container, text="Select Profile:")
profile_dropdown_label.pack(side="left", padx=5)

profile_dropdown = ttk.Combobox(filter_container)
profile_dropdown.pack(side="left", padx=5)


# Event handler for tree selection
def on_profile_select(event):
    global selected_profile
    selected_profile = profile_dropdown.get()
    fetch_profile_data(selected_profile)
    
profile_dropdown.bind("<<ComboboxSelected>>", on_profile_select)

# Create a button for profile creation
create_profile_button = tk.Button(filter_container, text="Create Profile", command=create_profile)
create_profile_button.pack(side="left", padx=10)

filter_container.pack(pady=10)

# Pack the Treeview
tree.pack(expand=True, fill="both")


# Dropdown menu for selecting options
tree_options = ["Gladiator Info", "Combat Stats", "Skills", "Background Info", "Health Info", "External Factors", "Outcome"]  # Add option names here
tree_selector = ttk.Combobox(nav_container, values=tree_options)
tree_selector.set(tree_options[0])  # Set default value
tree_selector.pack(side="left", padx=10)

# Initialize limit and selected_option
limit = 50  # Adjust the limit based on your requirements
selected_option = tree_options[0]  # Set the default option

# Event handler for tree selection
def on_tree_select(event):
    global selected_option
    selected_option = tree_selector.get()
    fetch_data_for_tree(selected_option)

# Bind the event handler to the tree_selector
tree_selector.bind("<<ComboboxSelected>>", on_tree_select)

# Pack the nav_container
nav_container.pack(pady=10)



# Entry to Go to a Specific Page
go_to_page_label = tk.Label(nav_container, text="Go to Page:")
go_to_page_label.pack(side="left", padx=5)

go_to_page_entry = tk.Entry(nav_container)
go_to_page_entry.pack(side="left", padx=5)

go_to_page_button = tk.Button(nav_container, text="Go", command=on_go_to_page)
go_to_page_button.pack(side="left", padx=5)

# Previous Button
previous_button = tk.Button(nav_container, text="Previous", command=on_previous)
previous_button.pack(side="left", padx=10)

# Create a label to display the current page number
current_page_label = tk.Label(nav_container, text="Page: 1")
current_page_label.pack(side="left", padx=10)

# Next Button
next_button = tk.Button(nav_container, text="Next", command=on_next)
next_button.pack(side="left", padx=10)

# Fetch data for the initial tree
fetch_data_for_tree(tree_selector.get())
fetch_profile_names()

# Run the Tkinter event loop
root.mainloop()
