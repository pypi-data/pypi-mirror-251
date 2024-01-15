# region Import Packages

from Utils.GeneralLists import dataBases

# endregion

# region Class DbConfig

class DbConfig:

    # region Global Variables

    dbUrl = None

    # endregion

    # region Init
    
    def __init__(self):

        self.__host = ''
        self.__userName = ''
        self.__password = ""

    # endregion

    # region Main
        
    def main(self, index):

        DbConfig.dbUrl = 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(user=self.__userName, pw=self.__password, url=self.__host, db=dataBases[index])
        
    # endregion
    
# endregion