import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from ttkthemes import ThemedTk
from functions.user_management import load_users, save_admin_account
from functions.ui_functions import *

class SecureDataHubApp:
    def __init__(self, root):
        """Initialisiert die Anwendung und zeigt den Login-Bildschirm an"""
        self.root = root
        self.root.title("SecureDataHub")
        self.root.geometry("1000x700")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#1e1e2e')
        self.style.configure('TButton', background='#4e4e7e', foreground='white', font=('Helvetica', 12, 'bold'))
        self.style.configure('TLabel', background='#1e1e2e', foreground='white', font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TCheckbutton', background='#1e1e2e', foreground='white', font=('Helvetica', 12))

        self.logged_in_user = None
        self.user_role = None
        self.users = load_users()
        self.compliance = Compliance()
        ensure_files_json_exists()
        self.login_screen()

    def login_screen(self):
        """Erstellt die Login-Oberfläche"""
        self.clear_screen()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Login", font=("Helvetica", 24, 'bold')).pack(pady=20)

        ttk.Label(frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.login).pack(pady=10)

        if not self.users:
            ttk.Button(frame, text="Create Admin Account", command=self.create_admin_account).pack(pady=10)

    def toggle_password(self):
        """Schaltet die Anzeige des Passworts um"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def create_admin_account(self):
        """Erstellt die Oberfläche zur Erstellung eines Admin-Accounts"""
        self.clear_screen()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Create Admin Account", font=("Helvetica", 24, 'bold')).pack(pady=20)

        ttk.Label(frame, text="Admin Username:").pack(pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(frame, text="Admin Password:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.pack(pady=5)

        ttk.Button(frame, text="Create Admin", command=self.save_admin_account).pack(pady=10)

    def save_admin_account(self):
        """Speichert den Admin-Account in der JSON-Datei"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            save_admin_account(username, password, self.users)
            messagebox.showinfo("Success", "Admin account created successfully!")
            self.login_screen()
        else:
            messagebox.showerror("Error", "Username and password cannot be empty.")

    def login(self):
        """Verifiziert die Anmeldeinformationen und zeigt die Hauptoberfläche an"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username]["password"] == password:
            self.logged_in_user = username
            self.user_role = self.users[username]["role"]
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password. You are not authorized to use this app.")

    def main_screen(self):
        """Erstellt die Hauptoberfläche der Anwendung"""
        self.clear_screen()

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="SecureDataHub", font=("Helvetica", 24, 'bold')).pack(pady=20)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, pady=10)

        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10)

        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10)

        if self.user_role == "admin":
            ttk.Button(left_frame, text="View User Data", command=lambda: view_user_data(self)).pack(pady=10)
            ttk.Button(left_frame, text="Add User", command=lambda: add_user(self)).pack(pady=10)
            ttk.Button(left_frame, text="Set Document Expiry", command=lambda: set_document_expiry(self)).pack(pady=10)
            ttk.Button(left_frame, text="Edit Policies", command=lambda: edit_policies(self)).pack(pady=10)
            ttk.Button(left_frame, text="Manage Notifications", command=lambda: manage_notifications(self)).pack(pady=10)
            ttk.Button(left_frame, text="Manage Users", command=lambda: manage_users(self)).pack(pady=10)
            ttk.Button(left_frame, text="Change User Role", command=lambda: change_user_role(self)).pack(pady=10)
            ttk.Button(left_frame, text="Send Notification", command=lambda: send_user_notification(self)).pack(pady=10)

        ttk.Label(right_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(right_frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(right_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_check.pack(pady=5)

        ttk.Button(right_frame, text="Encrypt File(s)", command=lambda: encrypt_files(self)).pack(pady=10)
        ttk.Button(right_frame, text="Decrypt File(s)", command=lambda: decrypt_files(self)).pack(pady=10)
        ttk.Button(right_frame, text="Check Compliance", command=lambda: check_compliance(self)).pack(pady=10)
        ttk.Button(right_frame, text="Share File Securely", command=lambda: share_file_securely(self)).pack(pady=10)
        ttk.Button(right_frame, text="Received Files", command=lambda: view_received_files(self)).pack(pady=10)
        ttk.Button(right_frame, text="User Activity Log", command=lambda: view_user_activity(self)).pack(pady=10)
        ttk.Button(right_frame, text="Logout", command=self.login_screen).pack(pady=10)

        notification_count = get_unread_notification_count(self)
        notification_text = f"Notifications ({notification_count})"
        self.notification_button = ttk.Button(main_frame, text=notification_text, command=lambda: manage_notifications(self))
        self.notification_button.pack(side=tk.TOP, pady=10)

        footer_frame = ttk.Frame(self.root, padding=10)
        footer_frame.pack(side='bottom', fill='x')

        self.footer_label = ttk.Label(footer_frame, text=f"Logged in as {self.logged_in_user} ({self.user_role}) - SecureDataHub by Mr H", font=("Helvetica", 10))
        self.footer_label.pack(side='left', padx=10)

        ttk.Button(footer_frame, text="Delete My Account", command=lambda: delete_my_account(self)).pack(side='right')

    def clear_screen(self):
        """Löscht alle Widgets von der aktuellen Oberfläche"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = SecureDataHubApp(root)
    root.mainloop()
