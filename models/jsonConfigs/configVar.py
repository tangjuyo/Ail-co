import json

class configVar:
    nom_fichier = "data/config.json"

    @staticmethod
    def lire_variables():
        with open(configVar.nom_fichier, 'r') as fichier:
            config = json.load(fichier)
        return config

    @staticmethod
    def lire_variable(nom_variable):
        config = configVar.lire_variables()
        if nom_variable in config:
            return config[nom_variable]
        else:
            return None
        
    @staticmethod
    def ecrire_variable(nom_variable, valeur_variable):
        config = configVar.lire_variables()
        config[nom_variable] = valeur_variable
        with open(configVar.nom_fichier, 'w') as fichier:
            json.dump(config, fichier, indent=4)

    @staticmethod
    def supprimer_variable(nom_variable):
        config = configVar.lire_variables()
        if nom_variable in config:
            del config[nom_variable]
            with open(configVar.nom_fichier, 'w') as fichier:
                json.dump(config, fichier, indent=4)

    @staticmethod
    def update_variable(nom_variable, nouvelle_valeur):
        config = configVar.lire_variables()
        if nom_variable in config:
            config[nom_variable] = nouvelle_valeur
            with open(configVar.nom_fichier, 'w') as fichier:
                json.dump(config, fichier, indent=4)

