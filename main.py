import tkinter as tk
from tkinter import messagebox

class RecipeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipe App")

        # Configure the window size and font
        self.master.geometry("400x300")
        self.master.option_add("*Font", "Courier 12")

        # Create and place widgets for the login screen
        self.label_username = tk.Label(master, text="Username:")
        self.label_password = tk.Label(master, text="Password:")
        self.entry_username = tk.Entry(master, font=("Courier", 14))
        self.entry_password = tk.Entry(master, show="*", font=("Courier", 14))
        self.button_login = tk.Button(master, text="Login", command=self.login, font=("Courier", 14))
        self.button_create_account = tk.Button(master, text="Create Account", command=self.create_account, font=("Courier", 14))

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
            self.show_recipe_app()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def create_account(self):
        #allows user to create an account
        pass

    def show_recipe_app(self):
        # Create and place widgets for the main recipe app
        # (unchanged from the previous version)
        pass

    def add_recipe(self):
        # Implement logic to add a new recipe (e.g., new window/form)
        messagebox.showinfo("Info", "Functionality to add recipes coming soon!")

def main():
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
