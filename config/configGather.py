import configparser


class configGather():
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)


    def getValue(self, section, key):
        try:
            return self.config[section][key]
        except AttributeError as e:
            print("Attribut Error : ", e)
            return None
        except KeyError as e:
            print("Key Error : ", e)
            return None

if __name__ == "__main__":
    config = configGather('./config.ini')
    print (config.getValue('SERVICE', 'UI'))
    print (config.getValue('SERVICE', 'SLACK'))
    print (config.getValue('SERVICE', 'CREON'))


            

