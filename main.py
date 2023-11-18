import tkinter as tk
from tkinter import ttk, messagebox

# Assume you have a customtkinter module with a CTkButton
from customtkinter import CTkButton

class RecipeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipe App")
        self.master.geometry("600x400")
        self.master.option_add("*Font", "Courier 12")

        # Initially, show the login page
        self.show_login_page()

    def show_login_page(self):
        # Create widgets for the login page
        self.label_username = tk.Label(self.master, text="Username:", font=("Courier", 14))
        self.label_password = tk.Label(self.master, text="Password:", font=("Courier", 14))
        self.entry_username = tk.Entry(self.master, font=("Courier", 14))
        self.entry_password = tk.Entry(self.master, show="*", font=("Courier", 14))
        self.button_login = CTkButton(self.master, text="Login", command=self.login, font=("Courier", 14))
        self.button_create_account = CTkButton(self.master, text="Create Account", command=self.show_create_account_page, font=("Courier", 14))

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=5)
        self.button_login.pack(pady=10)
        self.button_create_account.pack(pady=10)

    def login(self):
        # Implement your login authentication logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Dummy authentication, replace with database check
        if username == "example" and password == "password":
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
        self.button_submit = CTkButton(self.master, text="Submit", command=self.create_account, font=("Courier", 14))

        self.label_new_username.pack(pady=10)
        self.entry_new_username.pack(pady=5)
        self.label_new_password.pack(pady=10)
        self.entry_new_password.pack(pady=5)
        self.button_submit.pack(pady=10)

    def create_account(self):
        # Implement your account creation logic here
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()

        # Dummy account creation, replace with database insertion
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
        all_recipes_tab = ttk.Frame(self.notebook)
        add_recipe_tab = ttk.Frame(self.notebook)

        self.notebook.add(my_recipes_tab, text="My Recipes")
        self.notebook.add(all_recipes_tab, text="All Recipes")
        self.notebook.add(add_recipe_tab, text="Add Recipe")

        # Content for each tab
        self.create_my_recipes_tab(my_recipes_tab)
        self.create_all_recipes_tab(all_recipes_tab)
        self.create_add_recipe_tab(add_recipe_tab)

    def create_my_recipes_tab(self, tab):
        label = tk.Label(tab, text="Display My Recipes content here", font=("Courier", 16))
        label.pack(padx=20, pady=20)

    def create_all_recipes_tab(self, tab):
        label = tk.Label(tab, text="Display All Recipes content here", font=("Courier", 16))
        label.pack(padx=20, pady=20)

    def create_add_recipe_tab(self, tab):
        label = tk.Label(tab, text="Add Recipe Form", font=("Courier", 16))
        label.pack(pady=20)

        # Add Recipe Form Elements
        tk.Label(tab, text="Recipe Name:", font=("Courier", 12)).pack(pady=10)
        recipe_name_entry = tk.Entry(tab, font=("Courier", 12))
        recipe_name_entry.pack(pady=5)

        tk.Label(tab, text="Ingredients:", font=("Courier", 12)).pack(pady=10)
        ingredients_text = tk.Text(tab, height=5, width=40, font=("Courier", 12))
        ingredients_text.pack(pady=5)

        tk.Label(tab, text="Instructions:", font=("Courier", 12)).pack(pady=10)
        instructions_text = tk.Text(tab, height=8, width=40, font=("Courier", 12))
        instructions_text.pack(pady=5)

        # Use CTkButton from customtkinter instead of tk.Button
        add_button = CTkButton(tab, text="Add Recipe", command=lambda: self.add_recipe(recipe_name_entry.get(), ingredients_text.get("1.0", tk.END), instructions_text.get("1.0", tk.END)), font=("Courier", 14))
        add_button.pack(pady=20)

    def add_recipe(self, name, ingredients, instructions):
        # Add logic to save the recipe to the database
        messagebox.showinfo("Info", f"Recipe '{name}' added successfully!")

    def destroy_login_widgets(self):
        # Destroy login page widgets
        self.label_username.destroy()
        self.label_password.destroy()
        self.entry_username.destroy()
        self.entry_password.destroy()
        self.button_login.destroy()
        self.button_create_account.destroy()
    def destroy_create_account_widgets(self):
        # Destroy login page widgets
        self.label_new_username.destroy()
        self.label_new_password.destroy()
        self.entry_new_username.destroy()
        self.entry_new_password.destroy()
        self.button_submit.destroy()

def main():
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
