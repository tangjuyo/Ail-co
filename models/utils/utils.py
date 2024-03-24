import os,re
from email.header import decode_header


class Utils:
    
    # Fonction pour créer un dossier s'il n'existe pas
    @staticmethod
    def create_folder_if_not_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Fonction pour nettoyer les caractères invalides dans le nom de fichier
    @staticmethod
    def clean_string(string):
        clean_string = re.sub(r'[<>:"/\\|?*\n\r\t]�', '', string)
        return clean_string[:255]  # Limite la longueur du nom de fichier à 255 caractères pour la compatibilité du système de fichiers
    
    @staticmethod
    def decode_sender(sender):
        decoded_sender = ''
        parts = decode_header(sender)
        for part, charset in parts:
            if isinstance(part, bytes):
                # Sinon, décodez en utilisant le charset spécifié ou par défaut en UTF-8
                decoded_part = part.decode(charset or 'utf-8')
                decoded_sender += decoded_part
            else:
                decoded_sender += part
        return decoded_sender.strip()
    
    @staticmethod
    def extract_all_mail_from_path():
        return [item[len('entrepot_'):] for item in os.listdir("data/")]

    @staticmethod
    def extract_info_from_path(filepath):
        # Séparer le chemin en parties
        parts = filepath.split(os.sep)

        # Vérifier si le chemin est conforme à votre structure
        if len(parts) >= 5 and parts[0] == 'data' and parts[1].startswith('entrepot_'):
            # Extraire le nom de la boîte mail
            mail = parts[1][len('entrepot_'):]

            # Extraire la date
            date = parts[2]

            # Extraire l'expéditeur
            sender = parts[3]

            # Extraire le sujet du mail du nom du fichier
            subject = os.path.splitext(parts[-1])[0]
            
            return mail, date, sender,subject
        else:
            return None, None, None, None