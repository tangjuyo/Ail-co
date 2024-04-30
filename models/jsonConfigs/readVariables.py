import json

class readVariables:
    config_fichier = "data/config.json"
    language_folder = "data/language/"
    
    @staticmethod
    def initLanguage():
        return readVariables.language_folder + readVariables.lire_config_language_variable() + ".json"

    @staticmethod
    def lire_config_language_variable():
        with open(readVariables.config_fichier, 'r') as fichier:
            config = json.load(fichier)
        if "language" in config:
            return config["language"]
        else:
            return None
        
    @staticmethod
    def lire_variable(groupe, variable):
        with open(readVariables.initLanguage(), 'r') as fichier:
            config = json.load(fichier)
            return config[groupe][variable]
        
    @staticmethod
    def lire_global_variable_from_language(variable):
        
        with open(readVariables.initLanguage(), 'r') as fichier:
            config = json.load(fichier)
            return readVariables.get_key_from_value(config["CustomTreeWidget"],variable)

    @staticmethod 
    def get_key_from_value(json_data, value):
        for key, val in json_data.items():
            if val == value:
                return key
        return None

