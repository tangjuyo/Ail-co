import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class SQLiteDAO:
    def __init__(self, db_file, password):
        self.db_file = db_file
        self.password = password
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        try :
            # Créer la table pour les adresses e-mail et mots de passe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_password (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT,
                    iv_password TEXT
                )
            ''')
            # Créer la table si elle n'existe pas encore
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS mails (
                    id INTEGER PRIMARY KEY,
                    sender BLOB,
                    iv_sender BLOB,
                    subject BLOB,
                    iv_subject BLOB,
                    body BLOB,
                    iv_body BLOB,
                    folder TEXT,
                    mail TEXT,
                    date TEXT,
                    compiled_value TEXT UNIQUE
                )
            ''')
            self.conn.commit()
        except:
            print("table adresse existe déja")

    def encrypt_data(self, data):
        iv = os.urandom(16)
        cipher = AES.new(self.password.encode('utf-8'), AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return ct_bytes, iv

    def decrypt_data(self, encrypted_data, iv):
        cipher = AES.new(self.password.encode('utf-8'), AES.MODE_CBC, iv)
        try :
            pt_bytes = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            return pt_bytes.decode('utf-8')
        except :
            return encrypted_data

    def add_email_password(self, email, password):
        encrypted_password, iv = self.encrypt_data(password)
        cursor = self.conn.cursor()
        try :
            cursor.execute('''
                INSERT INTO email_password (email, password, iv_password)
                VALUES (?, ?, ?)
            ''', (email, encrypted_password, iv))
            self.conn.commit()
        except :
            print("adresse existe déja")

    def add_email(self, email):
        cursor = self.conn.cursor()
        encrypted_sender, iv_sender = self.encrypt_data(email[0])
        encrypted_subject, iv_subject = self.encrypt_data(email[1])
        try:
            encrypted_body, iv_body = self.encrypt_data(email[2])
        except:
            encrypted_body, iv_body = email[2], None
        
        uid = email[6]
        try:
            # Insérer les données dans la table correspondante
            cursor.execute(f'''
                INSERT INTO mails (sender, iv_sender, subject, iv_subject, body, iv_body, folder, mail, date,compiled_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (encrypted_sender, iv_sender, encrypted_subject, iv_subject, encrypted_body, iv_body, email[3], email[4], email[5], str(email[4]) + str(uid)))

            self.conn.commit()
        except:
            pass

    def get_emails(self):
        cursor = self.conn.cursor()
        decrypted_emails = []
        cursor.execute(f"SELECT * FROM mails")
        emails = cursor.fetchall()
        for email in emails:
            decrypted_sender = self.decrypt_data(email[1], email[2])
            decrypted_subject = self.decrypt_data(email[3], email[4])
            decrypted_body = self.decrypt_data(email[5], email[6])
            decrypted_email = [decrypted_sender, decrypted_subject, decrypted_body, email[7], email[8], email[9], email[10]]
            decrypted_emails.append(decrypted_email)
        return decrypted_emails

    def get_all_email_addresses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT email FROM email_password")
        email_addresses = cursor.fetchall()
        return [email[0] for email in email_addresses]
    
    def get_all_identifications(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT email, password,iv_password FROM email_password')
        rows = cursor.fetchall()
        email_password_pairs = []
        for row in rows:
            email = row[0]
            encrypted_password = row[1]
            iv = row[2]
            decrypted_password = self.decrypt_data(encrypted_password,iv)
            email_password_pairs.append((email, decrypted_password))
        return email_password_pairs
    
    def get_emails_for_address(self, address,folder):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM mails WHERE folder = ? AND mail = ?', (folder, address))
        emails = cursor.fetchall()
        decrypted_emails = []
        for email in emails:
            decrypted_sender = self.decrypt_data(email[1], email[2])
            decrypted_subject = self.decrypt_data(email[3], email[4])
            decrypted_body = self.decrypt_data(email[5], email[6])
            decrypted_email = Email(decrypted_sender, decrypted_subject, decrypted_body, email[7], email[8], email[9], email[10])
            decrypted_emails.append(decrypted_email)
        return decrypted_emails

    def mark_email_as_seen(self, email_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE emails SET mail_seen = 1 WHERE id = ?', (email_id,))
        self.conn.commit()

    def mark_email_as_unseen(self, email_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE emails SET mail_seen = 0 WHERE id = ?', (email_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
