import mysql.connector
import tkinter as tk
from tkinter import ttk

# Replace these values with your MySQL server details
host = "localhost"
user = "root"
password = "&%Bn96=mdQe4"
database = "gladiator"

# Function to fetch data for a specific tree
def fetch_data_for_tree(tree_option):
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

            # Fetch data for the selected tree
            query = f"SELECT * FROM gladiator.{tree_option.replace(' ', '').lower()};"
            mycursor.execute(query)
            result = mycursor.fetchall()

            # Clear existing data in the Treeview
            for row in tree.get_children():
                tree.delete(row)

            # Set column headings
            columns = get_columns_for_tree(tree_option)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
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

# Function to get columns for a specific tree
def get_columns_for_tree(tree_option):
    # Define your columns for each tree
    if tree_option == "Gladiator Info":
        return ("GladiatorID", "Name", "Age", "BirthYear", "Origin", "Height (cm)", "Weight (kg)")
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
columns = ("GladiatorID", "Name", "Age", "BirthYear", "Origin", "Height (cm)", "Weight (kg)")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Set column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col)  # Adjust the width as needed

# Configure the style for the Treeview widget
style = ttk.Style()
style.configure("Treeview", font=("Arial", 14))  # Adjust the font family and size as needed
style.configure("Treeview.Heading", font=("Arial", 14))

# Dropdown menu and fetch button container
container = ttk.Frame(root)

# Dropdown menu for selecting options
tree_options = ["Gladiator Info", "Combat Stats", "Skills", "Background Info", "Health Info", "External Factors", "Outcome"]  # Add your option names here
tree_selector = ttk.Combobox(container, values=tree_options)
tree_selector.set(tree_options[0])  # Set default value
tree_selector.pack(side="left", padx=10)

# Event handler for tree selection
def on_tree_select(event):
    selected_option = tree_selector.get()
    fetch_data_for_tree(selected_option)

# Fetch Button
fetch_button = tk.Button(container, text="Fetch Data", command=lambda: fetch_data_for_tree(tree_selector.get()))
fetch_button.pack(side="left", padx=10)

# Bind the event handler to the tree_selector
tree_selector.bind("<<ComboboxSelected>>", on_tree_select)

# Pack the container
container.pack(pady=10)

# Pack the Treeview
tree.pack(expand=True, fill="both")

# Fetch data for the initial tree
fetch_data_for_tree(tree_selector.get())

# Run the Tkinter event loop
root.mainloop()