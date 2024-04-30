from PySide6.QtWidgets import QApplication,QDialog
from vue.mainPage import mainPage
from controller.mailListController import mailListController
from vue.loginPage import PasswordInputDialog
from models.emailManager import EmailManager
import sys
from qt_material import apply_stylesheet


if __name__ == "__main__":
    # Création de l'application
    app = QApplication(sys.argv)

    # Création de la boîte de dialogue pour le mot de passe
    dialog = PasswordInputDialog()
    
    apply_stylesheet(dialog, theme='dark_red.xml')
    # Affichage de la boîte de dialogue et récupération du résultat
    result = dialog.exec()

    dialog.setpassword("@$WK10;Rw9JJV[+n")
    
    # Vérification si un mot de passe a été fourni
    if result == QDialog.Accepted:
        # Récupération du mot de passe
        password = dialog.password

        # Initialisation des modèles
        emailManager = EmailManager("data/database/database.db", password)

        # Création du contrôleur de gestion des mails
        mail_list_controller = mailListController(emailManager)
        
        # Création de la fenêtre principale et affichage
        window = mainPage(mail_list_controller)
        window.show()
        apply_stylesheet(app, theme='dark_red.xml')
        app.exec()