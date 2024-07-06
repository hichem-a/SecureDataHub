import tkinter as tk
from tkinter import filedialog, messagebox
from encrypt import encrypt
from decrypt import decrypt

class SecureDataHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureDataHub")
        self.root.geometry("500x400")
        self.root.configure(bg='#2e3f4f')

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="SecureDataHub", font=("Helvetica", 24, 'bold'), bg='#2e3f4f', fg='white').pack(pady=20)

        tk.Label(self.root, text="Password:", bg='#2e3f4f', fg='white').pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        self.encrypt_button = tk.Button(self.root, text="Encrypt File", command=self.encrypt_file, bg='#4caf50', fg='white')
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(self.root, text="Decrypt File", command=self.decrypt_file, bg='#f44336', fg='white')
        self.decrypt_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, bg='#607d8b', fg='white')
        self.exit_button.pack(pady=10)

        self.footer = tk.Label(self.root, text="This app was made by Mr. H", bg='#2e3f4f', fg='white', font=("Helvetica", 10))
        self.footer.pack(side='bottom', pady=10)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    data = file.read()
                password = self.password_entry.get()
                encrypted_data = encrypt(data.decode("latin1"), password)
                with open(file_path + ".enc", "w", encoding="utf-8") as file:
                    file.write(encrypted_data)
                messagebox.showinfo("Success", "File encrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encrypt file: {str(e)}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    encrypted_data = file.read()
                password = self.password_entry.get()
                decrypted_data = decrypt(encrypted_data, password)
                with open(file_path.replace(".enc", ""), "wb") as file:
                    file.write(decrypted_data)
                messagebox.showinfo("Success", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureDataHubApp(root)
    root.mainloop()
