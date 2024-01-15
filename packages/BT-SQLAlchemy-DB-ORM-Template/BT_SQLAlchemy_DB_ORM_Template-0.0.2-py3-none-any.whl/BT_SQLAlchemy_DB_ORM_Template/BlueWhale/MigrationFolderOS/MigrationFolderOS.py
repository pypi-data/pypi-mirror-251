# region Imports Packages

import shutil
import os

from Utils.GeneralLists import migrationFolderList

# endregion

# region Class MigrationFolderOS

class MigrationFolderOS:

    # region Init

    def __init__(self):

        self.__dirPath = os.getcwd()
    
    # endregion
    
    # region Change Folder

    def changeFolder(self, index):

        print("Database: ", self.__database)

        migrationsFolders = [folderName for folderName in os.listdir(self.__dirPath) if folderName.startswith("migrations")]

        diffFolderName = next((x for x in migrationFolderList if x not in migrationsFolders), None)

        self.renameFolder(diffFolderName, "migrations")
        self.renameFolder("migrations", migrationFolderList[index])

    # endregion
        
    # region renameFolder
   
    def renameFolder(self, newName, oldName):

        shutil.move(os.path.join(self.__dirPath, oldName), 
                  os.path.join(self.__dirPath, newName))
    
    # endregion

# endregion
