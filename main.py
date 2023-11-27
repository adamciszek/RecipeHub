import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont

# Assume you have a customtkinter module with a CTkButton
from customtkinter import CTkButton

import sqlite3

class RecipeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipe App")
        self.master.geometry("300x300")

        azonix_font = tkFont.Font(family="Azonix", size=12)
        self.master.option_add("*Font", azonix_font)

        self.logged_in_username = None

        # Initially, show the login page
        self.show_login_page()

        # Connect to the SQLite database (or create a new one if it doesn't exist)
        self.connection = sqlite3.connect("recipe_database.db")
        self.cursor = self.connection.cursor()

        # Create tables if they don't exist
        self.create_tables()

    def create_tables(self):
        # Create a 'users' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        # Create a 'recipes' table
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    name TEXT,
                    ingredients TEXT,
                    instructions TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

        # Commit the changes
        self.connection.commit()

    def show_login_page(self):
        # Create widgets for the login page
        self.label_username = tk.Label(self.master, text="Username:", font=("Courier", 14))
        self.label_password = tk.Label(self.master, text="Password:", font=("Courier", 14))
        self.entry_username = tk.Entry(self.master, font=("Courier", 14))
        self.entry_password = tk.Entry(self.master, show="*", font=("Courier", 14))
        self.button_login = CTkButton(self.master, text="Login", command=self.login, font=("Courier", 14))
        self.button_create_account = CTkButton(self.master, text="Create Account",
                                               command=self.show_create_account_page, font=("Courier", 14))

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=5)
        self.button_login.pack(pady=10)
        self.button_create_account.pack(pady=10)

        # Bind the Enter key to the login method
        self.master.bind('<Return>', lambda event: self.login())

    def login(self):
        # Implement your login authentication logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username and password match a record in the 'users' table
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            # Set the logged-in username
            self.logged_in_username = username

            # Destroy login page widgets
            self.destroy_login_widgets()

            # Show the main recipe app
            self.show_recipe_app()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_create_account_page(self):
        # Destroy login page widgets
        self.destroy_login_widgets()

        # Create widgets for the create account page
        self.label_new_username = tk.Label(self.master, text="New Username:", font=("Courier", 14))
        self.label_new_password = tk.Label(self.master, text="New Password:", font=("Courier", 14))
        self.entry_new_username = tk.Entry(self.master, font=("Courier", 14))
        self.entry_new_password = tk.Entry(self.master, show="*", font=("Courier", 14))

        # Visual message for password requirements
        self.password_requirements_label = tk.Label(self.master,
                                                    text="Password must be at least 6 characters with at least one capital letter.",
                                                    font=("Courier", 10), fg="gray")

        self.button_submit = CTkButton(self.master, text="Submit", command=self.create_account, font=("Courier", 14))

        self.label_new_username.pack(pady=10)
        self.entry_new_username.pack(pady=5)
        self.label_new_password.pack(pady=10)
        self.entry_new_password.pack(pady=5)

        # Pack the visual message
        self.password_requirements_label.pack(pady=5)

        self.button_submit.pack(pady=10)

    def create_account(self):
        # Implement your account creation logic here
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        # Check if the username already exists
        self.cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
            return

        # Check if the password meets the criteria
        if len(new_password) < 6 or not any(char.isupper() for char in new_password):
            # Display an error message based on the password criteria
            error_message = "Password must be at least 6 characters with at least one capital letter."
            if len(new_password) < 6:
                error_message = "Password must be at least 6 characters."
            elif not any(char.isupper() for char in new_password):
                error_message = "Password must contain at least one capital letter."
            messagebox.showerror("Error", error_message)
            return

        # Dummy account creation, replace with database insertion
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
        self.connection.commit()

        messagebox.showinfo("Info", f"Account '{new_username}' created successfully!")
        self.destroy_create_account_widgets()

        # After creating the account, show the login page again
        self.show_login_page()

    def show_recipe_app(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        my_recipes_tab = ttk.Frame(self.notebook)
        other_recipes_tab = ttk.Frame(self.notebook)
        add_recipe_tab = ttk.Frame(self.notebook)

        self.notebook.add(my_recipes_tab, text="My Recipes")
        self.notebook.add(other_recipes_tab, text="Other Recipes")
        self.notebook.add(add_recipe_tab, text="Add Recipe")

        # Content for each tab
        self.create_my_recipes_tab(my_recipes_tab)
        self.create_other_recipes_tab(other_recipes_tab)
        self.create_add_recipe_tab(add_recipe_tab)

        # Window size
        self.master.geometry("700x800")

    def create_my_recipes_tab(self, tab):
        # Get the user's ID from the stored username
        self.cursor.execute("SELECT id FROM users WHERE username=?", (self.logged_in_username,))
        user_id = self.cursor.fetchone()[0]

        # Retrieve the user's recipes from the 'recipes' table
        self.cursor.execute("SELECT name FROM recipes WHERE user_id=?", (user_id,))
        recipes = self.cursor.fetchall()

        # Display the recipe names
        for recipe in recipes:
            recipe_name_label = tk.Label(tab, text=recipe[0], font=("Courier", 14))
            recipe_name_label.pack(pady=5)
            recipe_name_label.bind("<Button-1>", lambda event, name=recipe[0]: self.show_recipe_details(name, tab))

    def show_recipe_details(self, recipe_name, tab):
        # Fetch the details of the selected recipe from the database
        self.cursor.execute("SELECT ingredients, instructions FROM recipes WHERE name=?", (recipe_name,))
        recipe_details = self.cursor.fetchone()

        # Create a new window to display the recipe details
        recipe_details_window = tk.Toplevel(self.master)
        recipe_details_window.title(recipe_name)

        # Display the recipe details in the new window
        tk.Label(recipe_details_window, text="Ingredients:", font=("Courier", 12)).pack(pady=5)
        tk.Label(recipe_details_window, text=recipe_details[0], font=("Courier", 12)).pack(pady=5)

        tk.Label(recipe_details_window, text="Instructions:", font=("Courier", 12)).pack(pady=5)
        tk.Label(recipe_details_window, text=recipe_details[1], font=("Courier", 12)).pack(pady=5)

    def create_other_recipes_tab(self, tab):
        # Get recipes created by other users
        other_recipes = self.get_other_users_recipes()

        # Display the recipe names
        for recipe in other_recipes:
            recipe_name_label = tk.Label(tab, text=recipe[0], font=("Courier", 14))
            recipe_name_label.pack(pady=5)
            recipe_name_label.bind("<Button-1>", lambda event, name=recipe[0]: self.show_recipe_details(name, tab))

    def get_other_users_recipes(self):
        # Get the user's ID from the stored username
        self.cursor.execute("SELECT id FROM users WHERE username=?", (self.logged_in_username,))
        user_id = self.cursor.fetchone()[0]

        # Retrieve recipes created by other users
        self.cursor.execute("SELECT name FROM recipes WHERE user_id != ?", (user_id,))
        recipes = self.cursor.fetchall()

        return recipes

    def create_add_recipe_tab(self, tab):
        label = tk.Label(tab, text="Add Recipe Form", font=("Courier", 16))
        label.pack(pady=20)

        # Add Recipe Form Elements
        tk.Label(tab, text="Recipe Name:", font=("Courier", 12)).pack(pady=10)
        self.recipe_name_entry = tk.Entry(tab, font=("Courier", 12))
        self.recipe_name_entry.pack(pady=5)

        tk.Label(tab, text="Ingredients:", font=("Courier", 12)).pack(pady=10)
        self.ingredients_entries = []  # List to store ingredient Entry widgets
        for i in range(5):  # You can adjust the number of ingredient Entry widgets as needed
            ingredient_entry = tk.Entry(tab, font=("Courier", 12))
            ingredient_entry.pack(pady=5)
            self.ingredients_entries.append(ingredient_entry)

        tk.Label(tab, text="Instructions:", font=("Courier", 12)).pack(pady=10)
        self.instructions_text = tk.Text(tab, height=8, width=40, font=("Courier", 12))
        self.instructions_text.pack(pady=5)

        # Use CTkButton from customtkinter instead of tk.Button
        add_button = CTkButton(tab, text="Add Recipe", command=self.add_recipe, font=("Courier", 14))
        add_button.pack(pady=20)

    def add_recipe(self):
        # Get the user's ID from the stored username
        self.cursor.execute("SELECT id FROM users WHERE username=?", (self.logged_in_username,))
        user_id = self.cursor.fetchone()[0]

        # Get the recipe details from the entry and text widgets
        name = self.recipe_name_entry.get()

        # Get the ingredients from the Entry widgets
        ingredients = "\n".join(entry.get() for entry in self.ingredients_entries)

        instructions = self.instructions_text.get("1.0", tk.END)

        # Check if title, ingredients, and steps are not empty
        if not name.strip() or not ingredients.strip() or not instructions.strip():
            messagebox.showerror("Error", "Please provide a title, ingredients, and steps for the recipe.")
            return

        # Add the recipe to the 'recipes' table
        self.cursor.execute("INSERT INTO recipes (user_id, name, ingredients, instructions) VALUES (?, ?, ?, ?)",
                            (user_id, name, ingredients, instructions))
        self.connection.commit()

        messagebox.showinfo("Info", f"Recipe '{name}' added successfully!")

        # Clear the text fields after adding the recipe
        self.recipe_name_entry.delete(0, tk.END)
        for entry in self.ingredients_entries:
            entry.delete(0, tk.END)
        self.instructions_text.delete("1.0", tk.END)

        # Update the content of the "My Recipes" tab
        self.update_my_recipes_tab()

    def update_my_recipes_tab(self):
        # Check if the "My Recipes" tab already exists
        my_recipes_tab_exists = False
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "My Recipes":
                my_recipes_tab_exists = True
                my_recipes_tab_id = tab_id
                break

        if my_recipes_tab_exists:
            # Destroy existing content of the "My Recipes" tab
            for widget in self.master.nametowidget(my_recipes_tab_id).winfo_children():
                widget.destroy()

            # Create and display the updated content for the "My Recipes" tab
            self.create_my_recipes_tab(self.master.nametowidget(my_recipes_tab_id))
        else:
            # Create a new frame for the "My Recipes" tab
            my_recipes_tab = ttk.Frame(self.notebook)
            self.notebook.add(my_recipes_tab, text="My Recipes")

            # Create and display the content for the "My Recipes" tab
            self.create_my_recipes_tab(my_recipes_tab)

    def destroy_login_widgets(self):
        # Destroy login page widgets
        self.label_username.destroy()
        self.label_password.destroy()
        self.entry_username.destroy()
        self.entry_password.destroy()
        self.button_login.destroy()
        self.button_create_account.destroy()

    def destroy_create_account_widgets(self):
        # Destroy create account page widgets
        self.label_new_username.destroy()
        self.label_new_password.destroy()
        self.entry_new_username.destroy()
        self.entry_new_password.destroy()
        self.password_requirements_label.destroy()
        self.button_submit.destroy()

def main():
    root = tk.Tk()
    app = RecipeApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
