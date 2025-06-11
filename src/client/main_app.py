import tkinter as tk
from tkinter import messagebox
from ui.login import LoginUI
from ui.dashboard import DashboardUI
from ui.search import SearchUI
from ui.upload import UploadUI
from ui.add_user import AddUserUI
import requests
import json
from abe_core import SelfAES, ABE, objectToBytes, bytesToObject
from base64 import b64encode, b64decode
import os

AUTHORITY_SERVER = "http://127.0.0.1:5050"
STORAGE_SERVER = "http://127.0.0.1:8000"

class HealthcareApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_user = None
        self.current_role = None
        self.current_token = None
        self.current_ui = None
        self.dashboard_ui = None
        self.session = requests.Session() 
        
        # Add ABE components from first version
        self.abe = ABE()
        self.self_aes = SelfAES()
        
        self.show_login()
    
    # Add ABE helper methods from first version
    def encrypt_data(self, data, policy):
        """Encrypt data using ABE with specified policy"""
        try:
            data_bytes = objectToBytes(data)
            encrypted_data = self.abe.encrypt(data_bytes, policy)
            return b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt data: {str(e)}")
            return None
    
    def decrypt_data(self, encrypted_data, user_attributes):
        """Decrypt ABE encrypted data using user attributes"""
        try:
            encrypted_bytes = b64decode(encrypted_data.encode('utf-8'))
            decrypted_bytes = self.abe.decrypt(encrypted_bytes, user_attributes)
            return bytesToObject(decrypted_bytes)
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Failed to decrypt data: {str(e)}")
            return None

    def show_login(self):
        self.clear_current_ui()
        self.login_ui = LoginUI(self.root, self.handle_login)
    
    def handle_login(self, username, password):
        try:
            login_data = {
                'username': username,
                'password': password
            }
            
            login_response = requests.post(
                f"{AUTHORITY_SERVER}/login",
                data={'username': username, 'password': password},
                timeout=10
            )
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                self.current_user = response_data.get('username')
                self.current_role = response_data.get('role')
                self.current_token = response_data.get('token')
                
                # Store user attributes for ABE decryption
                self.user_attributes = response_data.get('attributes', [])
                
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")
                
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {str(e)}")

    
    def determine_role(self, attributes):
        """Determine the highest privilege role from attributes"""
        role_priority = ['admin', 'doctor', 'nurse', 'researcher', 'patient']
        for role in role_priority:
            if role in attributes:
                return role
        return 'patient'  
    
    def show_dashboard(self):
        """Display the main dashboard"""
        self.clear_current_ui()
        
        button_callbacks = {
            'search': self.show_search,
            'upload': self.show_upload,
            'logout': self.handle_logout,
            'add_user': self.show_add_user if self.current_role == 'admin' else None
        }
        
        try:
            self.dashboard_ui = DashboardUI(
                self.root, 
                self.current_user, 
                self.current_role, 
                button_callbacks
            )
            self.current_ui = self.dashboard_ui
        except Exception as e:
            messagebox.showerror("Dashboard Error", f"Failed to load dashboard: {str(e)}")
    
    def show_search(self):
        """Display the search interface"""
        if self.dashboard_ui and hasattr(self.dashboard_ui, 'content_frame'):
            try:
                self.search_ui = SearchUI(
                    self.dashboard_ui.content_frame, 
                    self.handle_search
                )
            except Exception as e:
                messagebox.showerror("Search UI Error", f"Failed to load search interface: {str(e)}")
        else:
            messagebox.showerror("Error", "Dashboard not properly initialized")
    
    def show_upload(self):
        """Display the upload interface"""
        if self.dashboard_ui and hasattr(self.dashboard_ui, 'content_frame'):
            try:
                self.upload_ui = UploadUI(
                    self.dashboard_ui.content_frame, 
                    self.handle_upload,
                )
            except Exception as e:
                messagebox.showerror("Upload UI Error", f"Failed to load upload interface: {str(e)}")
        else:
            messagebox.showerror("Error", "Dashboard not properly initialized")
    
    def show_add_user(self):
        """Display the add user interface for admin"""
        if self.dashboard_ui and hasattr(self.dashboard_ui, 'content_frame'):
            try:
                self.add_user_ui = AddUserUI(
                    self.dashboard_ui.content_frame, 
                    self.handle_add_user
                )
            except Exception as e:
                messagebox.showerror("Add User Error", f"Failed to load add user interface: {str(e)}")
        else:
            messagebox.showerror("Error", "Dashboard not properly initialized")

    def handle_add_user(self, user_data):
        """Handle adding a new user"""
        try:
            if not self.current_token:
                messagebox.showerror("Error", "Not authenticated")
                return
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def handle_search(self, search_criteria):
        """Handle patient data search with ABE decryption"""
        try:
            search_response = requests.post(
                f"{STORAGE_SERVER}/search",
                json=search_criteria,
                headers={'Authorization': f'Bearer {self.current_token}'}
            )
            
            if search_response.status_code == 200:
                encrypted_results = search_response.json().get('results', [])
                
                # Decrypt each result using user attributes
                decrypted_results = []
                for encrypted_result in encrypted_results:
                    decrypted_data = self.decrypt_data(
                        encrypted_result['data'], 
                        self.user_attributes
                    )
                    
                    if decrypted_data:
                        decrypted_results.append(decrypted_data)
                
                # Display results in UI
                self.display_search_results(decrypted_results)
                
            else:
                messagebox.showerror("Search Failed", "Could not retrieve data")
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Search failed: {str(e)}")

    
    def handle_upload(self, upload_params):
        """Handle file upload functionality"""
        messagebox.showinfo("Info", "Upload feature not implemented yet")
    
    def logout(self):
        """Handle user logout and cleanup"""
        try:
            # Send logout request to server
            self.session.post(
                f"{AUTHORITY_SERVER}/logout",
                headers={'Authorization': f'Bearer {self.current_token}'}
            )
        except Exception as e:
            print(f"Logout error: {e}")
        finally:
            # Clean up session data
            self.current_user = None
            self.current_role = None
            self.current_token = None
            self.user_attributes = []
            self.session.close()
            self.show_login()
        
    def clear_current_ui(self):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
        except Exception as e:
            print(f"Error clearing UI: {e}")
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

if __name__ == "__main__":
    try:
        app = HealthcareApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")