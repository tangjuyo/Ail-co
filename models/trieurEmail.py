import models.jsonConfigs.configVar as configVar

class TrieurEmail:
    def __init__(self, emails):
        self.emails = emails

    def trier_par_sender(self):
        if configVar.lire_variable("sortOrder") == True:
            return self.emails.sort_values(by='sender')
        return self.emails.sort_values(by='sender',ascending=False)

    def trier_par_date(self):
        if configVar.lire_variable("sortOrder") == True:
            return self.emails.sort_values(by='date')
        return self.emails.sort_values(by='date',ascending=False)

    def trier_par_sujet(self):
        if configVar.lire_variable("sortOrder") == True:
            return self.emails.sort_values(by='subject')
        return self.emails.sort_values(by='subject',ascending=False)
        
    def updateEmails(self,emails):
        self.emails = emails
