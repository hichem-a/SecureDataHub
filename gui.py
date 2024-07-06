import tkinter as tk
from tkinter import filedialog, messagebox
from encryption import encrypt, decrypt

class SecureDataHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureDataHub")
        self.root.geometry("400x300")

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:  # Binärmodus
                data = file.read()
            password = self.password_entry.get()
            encrypted_data = encrypt(data.decode("latin1"), password)  # Nutzung eines generischen Encodings
            with open(file_path + ".enc", "w", encoding="utf-8") as file:  # Schreiben als Textdatei
                file.write(encrypted_data)
            messagebox.showinfo("Success", "File encrypted successfully!")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:  # Lesen als Textdatei
                encrypted_data = file.read()
            password = self.password_entry.get()
            try:
                decrypted_data = decrypt(encrypted_data, password).encode("latin1")  # Rückkonvertierung zu Binärdaten
                with open(file_path.replace(".enc", ""), "wb") as file:  # Binärmodus
                    file.write(decrypted_data)
                messagebox.showinfo("Success", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", "Failed to decrypt file: " + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureDataHubApp(root)
    root.mainloop()
