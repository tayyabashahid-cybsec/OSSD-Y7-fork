import tkinter as tk
from tkinter import messagebox
def read_file():
    try:
        data_file = open("login_data.txt", "r")
        records = data_file.readlines()
        data_file.close()
        return records
    except FileNotFoundError:
        return []

def write_file():
    data_file = open("login_data.txt", "a")
    data_file.write(user_input.get() + ";" + pass_input.get() + "\n")
    data_file.close()
    


def login():
    records = read_file()
    for record in records:
        username, password = record.strip().split(";")
        if user_input.get() == username and pass_input.get() == password:
            messagebox.showinfo("Success", "Login successful")
            user_input.delete(0, tk.END)
            pass_input.delete(0, tk.END) 
            return
def signup():
    if user_input.get() == "" or pass_input.get() == "":
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    write_file() 
    messagebox.showinfo("Success", "Account created successfully")
    user_input.delete(0, tk.END)
    pass_input.delete(0, tk.END) 

def main():
    pass

root = tk.Tk()
root.title("Login System")    
root.geometry("400x400")
root.configure(bg="white")
main_name = tk.Label(root, text="Welcome to my app",font = ("Comic Sans MS", 16, "bold"), bg="white")
main_name.pack(pady=20)
login_frame = tk.Frame(root, bg="white", padx=20, pady=20)
login_frame.pack()
name_l = tk.Label(login_frame, text="Username :", bg="white", font=("Times New Roman", 12, "bold"))
name_l.grid(row=0, column=0, padx=10, pady=10, sticky="w")
user_input = tk.Entry(login_frame, bg="lightblue", font=("Times New Roman", 12))
user_input.grid(row=0, column=1, padx=10, pady=10)
pas_l = tk.Label(login_frame, text="Password :", bg="white", font=("Times New Roman", 12, "bold"))
pas_l.grid(row=1, column=0, padx=10, pady=10, sticky="w")
pass_input = tk.Entry(login_frame, show="*", bg="lightblue", font=("Times New Roman", 12))
pass_input.grid(row=1, column=1, padx=10, pady=10)
button_frame = tk.Frame(login_frame, bg="white")
button_frame.grid(row=2, column=0, columnspan=2, pady=20)
login_button = tk.Button(button_frame, text="Login", bg='lightblue', width=10, command=login)
login_button.pack(side="left", padx=10)
signup_button = tk.Button(button_frame, text="Signup", bg="lightblue", width=10, command=signup)
signup_button.pack(side="left", padx=10)

root.mainloop()