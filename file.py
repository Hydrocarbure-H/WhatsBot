class File:

    def __init__(self):
        self.__file = open("last_message", "r+")

    def __del__(self):
        self.__file.close()

    def write(self, text):
        self.__file.seek(0)
        self.__file.write(text)

    def read(self):
        return self.__file.read()
