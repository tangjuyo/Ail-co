class Email:
    def __init__(self, sender, subject, body,folder,mail,date,uid):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.folder = folder
        self.mail = mail
        self.date = date
        self.uid = uid

    # Getter pour l'expéditeur
    def get_sender(self):
        return self.sender

    # Setter pour l'expéditeur
    def set_sender(self, sender):
        self.sender = sender

    # Getter pour le sujet
    def get_subject(self):
        return self.subject

    # Setter pour le sujet
    def set_subject(self, subject):
        self.subject = subject

    # Getter pour le corps
    def get_body(self):
        return self.body

    # Setter pour le corps
    def set_body(self, body):
        self.body = body

    # Getter pour le corps
    def get_mail(self):
        return self.mail

    # Setter pour le corps
    def set_mail(self, mail):
        self.body = mail

    # Getter pour le corps
    def get_date(self):
        return self.date

    # Setter pour le corps
    def set_date(self, date):
        self.body = date

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid
    
    def get_folder(self):
        return self.folder

    def set_folder(self, folder):
        self.folder = folder

    def __str__(self):
        return f"Sender: {self.sender}\nSubject: {self.subject}\nBody: {self.body}\folder: {self.folder}\nMail: {self.mail}\nDate: {self.date}\nUID: {self.uid}"