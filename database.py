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

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

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

# Dropdown menu and fetch button container
container = ttk.Frame(root)

# Dropdown menu for selecting options
tree_options = ["Gladiator Info", "Combat Stats", "Skills", "Background Info", "Health Info", "External Factors", "Outcome"]  # Add your option names here
tree_selector = ttk.Combobox(container, values=tree_options)
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

# Pack the container
container.pack(pady=10)

# Pack the Treeview
tree.pack(expand=True, fill="both")

# Fetch data for the initial tree
fetch_data_for_tree(tree_selector.get())

# Entry to Go to a Specific Page
go_to_page_label = tk.Label(container, text="Go to Page:")
go_to_page_label.pack(side="left", padx=5)

go_to_page_entry = tk.Entry(container)
go_to_page_entry.pack(side="left", padx=5)

go_to_page_button = tk.Button(container, text="Go", command=on_go_to_page)
go_to_page_button.pack(side="left", padx=5)

# Previous Button
previous_button = tk.Button(container, text="Previous", command=on_previous)
previous_button.pack(side="left", padx=10)

# Next Button
next_button = tk.Button(container, text="Next", command=on_next)
next_button.pack(side="left", padx=10)

# Run the Tkinter event loop
root.mainloop()
