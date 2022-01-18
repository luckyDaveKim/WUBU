class Result:
    def __init__(self, value, description):
        self.__value = value
        self.__description = description

    def get_value(self):
        return self.__value

    def get_description(self):
        return self.__description

    def __eq__(self, other):
        return self.get_value() == other.get_value()