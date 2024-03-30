import email
import os
from datetime import datetime
from email.header import decode_header
from models.utils import utils
import imapclient
import time

class Email_Parser:

    def __init__(self, address_mail, mdp, provider) -> None :
        self.address_mail = address_mail
        self.mdp = mdp
        self.provider = provider
        self.mail = imapclient.IMAPClient(provider, ssl=True)
        self.main_folder = "data/entrepot_" + self.address_mail
        self.folder_to_category = {
            "Inbox": "Boîte de réception",
            "INBOX": "Boîte de réception",
            "INBOX/OUTBOX": "Éléments envoyés",
            "Sent": "Éléments envoyés",
            "INBOX/TRASH": "Éléments supprimés",
            "Deleted": "Éléments supprimés",
            "Junk": "Spam",
            "[Gmail]/Spam": "Spam"
        }
        self.login()
        self.attachments = []
    
    def login(self):
        self.mail.login(self.address_mail, self.mdp)
        

    def close(self):
        self.mail.close_folder()
        self.mail.logout()
    
    def getDateMail(self,msg):
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            folder_date = local_date.strftime('%Y-%m-%d')
        else:
            # Si la date n'est pas disponible, utilisez la date actuelle
            folder_date = datetime.now().strftime('%Y-%m-%d')
        return folder_date
    
    def getSubjectMail(self,msg):
        string = msg
        encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252', 'us-ascii', 'iso-8859-15', 'utf-16', 'utf-8-sig', 'utf-16-le', 'utf-16-be', 'iso-2022-jp', 'shift_jis', 'euc-jp', 'iso-2022-kr', 'euc-kr', 'gb18030', 'gbk', 'big5', 'big5hkscs', 'iso-8859-2', 'iso-8859-7']

        for encoding in encodings_to_try:
            try:
                decoded_parts = [part[0].decode(part[1] or encoding) if isinstance(part[0], bytes) else part[0] for part in decode_header(string)]
                string_decoded = ''.join(decoded_parts)
                return string_decoded
            except Exception:
                pass  # Passer à l'encodage suivant s'il y a une erreur
        return "Bad string Found"  # Aucun encodage n'a fonctionné
    
    def downloadAttachment(self,attachments,part,sender_folder):
        # Pièce jointe
        attachment_name = decode_header(part.get_filename())[0][0]

        if attachment_name:
            #attachments.append(attachment_name)
            # Enregistrer la pièce jointe dans le dossier de l'e-mail
            attachment_path = os.path.join(sender_folder, attachment_name)
            with open(attachment_path, 'wb') as f:
                f.write(part.get_payload(decode=True))


    def getAllMails(self):
        start_time = time.time()
        allEmails = []
        for folder in self.mail.list_folders():
            allEmails += self.getAllMailsFromFolder(folder[-1])
            
        end_time = time.time()
        
        # Calcul du temps écoulé en secondes
        elapsed_time = end_time - start_time

        # Affichage du temps écoulé
        print("Temps écoulé :", elapsed_time, "secondes")
        return allEmails


    def getAllMailsFromFolder(self,folder,batch_size=100):
        
        emails = []
        # Si le folder n'est pas reconnu comme un category de l'application return tab vide (ne pas chercher de mails que l'ont va pas traiter)
        try:
            category = self.folder_to_category[folder]
        except :
            return emails
        
        self.mail.select_folder(folder)
        ids = self.mail.search(['ALL'])

        # Parcourir les e-mails par lots
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            raw_emails = self.mail.fetch(batch_ids, ['RFC822'])

            for email_id, raw_email in raw_emails.items():
                msg_data = raw_email[b'RFC822']
                msg = email.message_from_bytes(msg_data)


                # Récupérer l'expéditeur de l'e-mail
                decoded_sender = self.getSubjectMail(msg['From'])
                #decoded_sender = utils.Utils.decode_sender(sender)
                #decoded_sender = utils.Utils.clean_string(decoded_sender)
                # Décoder le sujet de l'e-mail
                subject_decoded= self.getSubjectMail(msg['Subject'])
                
                # Récupérer le corps du message HTML
                html_body = None
                self.attachments = []  # Pour stocker les noms des pièces jointes
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        try:
                            html_body = part.get_payload(decode=True).decode(part.get_content_charset())
                        except:
                            html_body = part.get_content_charset()
                        
                        try :
                            save_email = [decoded_sender,subject_decoded,html_body,category,self.address_mail,self.getDateMail(msg),email_id]
                            emails.append(save_email)
                        except :
                            print(folder)

                    elif part.get_content_maintype() != 'multipart' and part.get('Content-Disposition'):
                        try :
                            attachment_name = decode_header(part.get_filename())[0][0]
                            self.attachments.append(attachment_name)
                        except:
                            pass
                        # Créer le dossier pour la date si nécessaire
                        #utils.Utils.create_folder_if_not_exists(os.path.join(self.main_folder, string_date))
                        # Créer un dossier pour l'expéditeur
                        #date_folder = os.path.join(self.main_folder, string_date)
                        #utils.Utils.create_folder_if_not_exists(date_folder)
                        #self.downloadAttachment(attachments,part,date_folder)
                        
        return emails