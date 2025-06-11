from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from app.login import Ui_LoginWindow
from app.menu import Ui_MenuWindow
from app.search import Ui_SearchWindow
from app.push_data import Ui_PushWindow
from app.update_data import Ui_UpdateWindow
from app.view import Ui_ViewWindow
from urllib.parse import urljoin
import requests
import os

from abe_core import SelfAES, ABE, objectToBytes, bytesToObject
from base64 import b64encode, b64decode

TRUSTED_AUTHORITY = "http://localhost:5000" 
CLOUD_DOMAIN = "http://localhost:8000"

session = requests.Session()

class MainWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()

        data = {
            'username': username,
            'password': password
        }
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/login'), data=data)

        if response.status_code == 200:
            data = response.json()
            
            self.uid_text = str(data['ID'])
            
            self.show_menu()
            self.init_keys(data)
        else:
            self.popup(response.text)

    def show_menu(self):
        w = Ui_MenuWindow()
        w.setupUi(self)
        w.text_label.setText("UID: " + self.uid_text)
        
    def init_keys(self, data):
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/token'), json=data)
        self.token = response.text
        self.attribute = data['attribute']
        
        temp = []
        for attr in self.attribute:
            if attr == 'patient':
                temp.append('PATIENT'+str(data['ID']))
            else:
                temp.append(attr)
        self.attribute = [attr.upper().replace('_', '') for attr in temp]
        
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/get_keys'), json={'attribute': str(self.attribute)})
        keys = response.json()
        self.dk_key = keys['dk_key']
        self.pk_key = keys['pk_key']


    @pyqtSlot()
    def on_search_button_clicked(self):
        self.show_search()
    
    def show_search(self):
        w = Ui_SearchWindow()
        w.setupUi(self)
        self.search_combo_box = w.combo_box
        self.search_userid = w.userid_textbox
        self.search_name = w.name_textbox
    
    @pyqtSlot()
    def on_search_api_button_clicked(self):
        headers = {'Authorization': self.token}
        data = {
            'uid': self.search_userid.text(),
            'patient_name': self.search_name.text(),
            'collection_name': self.search_combo_box.currentText()
        }
        
        response = session.post(urljoin(CLOUD_DOMAIN, '/api/search_record'), json=data, headers=headers)
    
        data = response.json()
        if response.status_code != 200:
            self.popup(data['error'])
        else:
            self.popup_table(data)
        
    def popup_table(self, data):
        window = QDialog(self)
        window.setWindowTitle("Search Results")

        table = QTableWidget()
        table.setColumnCount(len(data[0])) 
        table.setRowCount(len(data))

        headers = list(data[0].keys())
        table.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(col_data))
                table.setItem(row_num, col_num, item)

        layout = QVBoxLayout()
        layout.addWidget(table)
        window.setLayout(layout)
        window.exec()
 
    @pyqtSlot()
    def on_view_button_clicked(self):
        self.show_view()
    
    def show_view(self):
        w = Ui_ViewWindow()
        w.setupUi(self)
        self.view_uid = w.UID
        self.view_combo_box = w.collection
    
    @pyqtSlot()
    def on_view_api_button_clicked(self):
        headers = {'Authorization': self.token}
        data = {
            'uid': self.view_uid.text(),
            'collection_name': self.view_combo_box.currentText()
        }
        response = session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
        
        data = response.json()
        if response.status_code != 200:
            self.popup(data['error'])
        else:
            try:
                if data['patient_data'] == []:
                    raise Exception('None')

                patient_data = data['patient_data'][0]
                
                enc_data = patient_data['file_data'].encode()
                plain, msg = self.decrypt_phase(enc_data)
                
                if plain:
                    DOWNLOAD_PATH = './download/'
                    file_name = patient_data['file_name']
                    with open(DOWNLOAD_PATH+file_name, 'wb') as file:
                        file.write(plain)  
                        
                    msg = "UID: " + patient_data['uid'] + '\n' + \
                        "Patient Name: " + patient_data['patient_name'] + '\n' + \
                        "Attachment Name: " + patient_data['file_name'] + \
                        '\nThe attachment has been downloaded successfully in "download/"'
                            
                    self.popup(msg, title="SUCCESS")
                elif plain == False:
                    self.popup(msg)
            except Exception as e:
                if str(e) == 'None':
                    self.popup("There's no data with the provided UID.\nPlease generate a profile for it.")    
                else:
                    print(e)
                    
    @pyqtSlot()
    def on_upload_button_clicked(self):
        self.show_push()
    
    def show_push(self):
        w = Ui_PushWindow()
        w.setupUi(self)
        self.push_uid = w.UID
        self.push_name = w.NAME
        self.file_name = w.FileName
        self.combo_box = w.collection
    
    @pyqtSlot()
    def on_push_button_clicked(self):
        if os.path.isfile(self.file_name.text()):
            headers = {'Authorization': self.token}
            
            UPDATE_POLICIES = {
                'health_record': ['doctor', 'nurse', 'patient'],
                'medicine_record': ['doctor', 'pharmacist', 'patient'],
                'financial_record': ['financial'],
                'research_record': ['doctor', 'researcher'],
            }    
                    
            POLICY = UPDATE_POLICIES[self.combo_box.currentText()]        
            user_attr = [attr.lower() for attr in self.attribute]
            final_policy = self.convert_policy(POLICY, user_attr, self.push_uid.text())
            
            with open(self.file_name.text(), 'rb') as file:
                file_data = file.read()
            enc_data = self.encrypt_phase(final_policy, file_data)
            
            patient_data = {
                'uid': self.push_uid.text(),
                'patient_name': self.push_name.text(),
                'file_name': self.file_name.text().split('/')[-1],
                'file_data': enc_data.decode()
            }
            data = {
                'collection_name': self.combo_box.currentText(),
                'patient_data': patient_data
            }
            response = session.post(urljoin(CLOUD_DOMAIN, '/api/upload_patient_record'), json=data, headers=headers)
            
            data = response.json()
            if response.status_code != 200:
                self.popup(data['error'])
            else:
                self.popup(data['message'], title="SUCCESS")
        else:
            self.popup("The file is not exist.\nPlease check the path again!")
    
    
    @pyqtSlot()
    def on_update_button_clicked(self):
        self.show_update()

    def show_update(self):
        w = Ui_UpdateWindow()
        w.setupUi(self)
        self.update_uid = w.UID
        self.update_name = w.NAME
        self.update_file_name = w.FileName
        self.update_combo_box = w.collection

    @pyqtSlot()
    def on_update_api_button_clicked(self):
        if os.path.isfile(self.update_file_name.text()):
            headers = {'Authorization': self.token}
            
            # Decrypt data to check if user be able to update
            
            data = {
                'uid': self.update_uid.text(),
                'collection_name': self.update_combo_box.currentText()
            }
            response = session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
            
            data = response.json()
            if response.status_code != 200:
                self.popup(data['error'])
            else:
                patient_data = data['patient_data'][0]
        
                enc_data = patient_data['file_data'].encode()
                plain, msg = self.decrypt_phase(enc_data)
                if plain is not False:

                # Encrypt data to Update
                
                    UPDATE_POLICIES = {
                        'health_record': ['doctor', 'nurse', 'patient'],
                        'medicine_record': ['doctor', 'pharmacist', 'patient'],
                        'financial_record': ['financial'],
                        'research_record': ['doctor', 'researcher'],
                    }    
                    
                    POLICY = UPDATE_POLICIES[self.update_combo_box.currentText()]        
                    user_attr = [attr.lower() for attr in self.attribute]
                    final_policy = self.convert_policy(POLICY, user_attr, self.update_uid.text())
                    
                    with open(self.update_file_name.text(), 'rb') as file:
                        file_data = file.read()
                    enc_data = self.encrypt_phase(final_policy, file_data)
                    
                    patient_data = {
                        'uid': self.update_uid.text(),
                        'patient_name': self.update_name.text(),
                        'file_name': self.update_file_name.text().split('/')[-1],
                        'file_data': enc_data.decode()
                    }
                    data = {
                        'collection_name': self.update_combo_box.currentText(),
                        'updated_data': patient_data
                    }
                    response = session.post(urljoin(CLOUD_DOMAIN, '/api/update_patient_record'), json=data, headers=headers)
                    
                    data = response.json()
                    if response.status_code != 200:
                        self.popup(data['error'])
                    else:
                        self.popup(data['message'], title="SUCCESS")
                else:
                    self.popup("You don't have permission to update the data!")
        else:
            self.popup("The file is not exist.\nPlease check the path again!")
    
    def convert_policy(self, policy, user_attr, text):

        final_policy = []
        for p in policy:
            tmp = 0
            for p2 in user_attr:
                if p in p2:
                    final_policy.append(p2)
                    tmp = 1
                    continue
            if p == 'patient':
                p = "{}_{}".format(p, text)
            if tmp == 0:
                final_policy.append(p)       

        final_policy = [p.replace('_', '').lower() for p in list(set(final_policy))]
        final_policy = ' or '.join(final_policy)
        
        return final_policy
    
    def encrypt_phase(self, final_policy, file_data):
        aes = SelfAES() ; abe = ABE()
        enc = b64encode(aes.encrypt(file_data))
        key = aes.getKey()
        enc_key = abe.encrypt(self.pk_key, key, final_policy)
        enc_key = objectToBytes(enc_key, abe.group)
        enc_data = enc_key + abe.sign + enc
        
        return enc_data
    
    def decrypt_phase(self, enc_data):
        aes = SelfAES(); abe = ABE()
        enc_key = enc_data.split(abe.sign)[0]
        enc = enc_data.split(abe.sign)[1]
        enc_key = bytesToObject(enc_key, abe.group)
        
        try:
            enc_key = abe.decrypt(self.pk_key, self.dk_key, enc_key)
            try:
                plain = aes.decrypt(b64decode(enc), enc_key)   
                return plain, "SUCCESS"
            except:
                return False, "Failed to decrypt the data. Please try again"
        except:
            return False, "You don't have permission to decrypt the data!"
            
    
    @pyqtSlot()
    def on_back_button_clicked(self):
        self.show_menu()
    
    def popup(self, message, title="ERROR"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()