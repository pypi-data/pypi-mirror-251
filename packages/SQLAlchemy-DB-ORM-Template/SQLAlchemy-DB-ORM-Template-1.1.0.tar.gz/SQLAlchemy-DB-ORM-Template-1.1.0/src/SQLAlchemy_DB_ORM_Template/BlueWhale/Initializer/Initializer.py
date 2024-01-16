# region Import Packages

import shutil
import os

from Utils.GeneralLists import migrationFolderList

# endregion

# region Initializer Class

class Initializer:

    # region Init

    def __init__(self):

        self.__dirPath = os.getcwd()
    
    # endregion
        
    # region Main

    def main(self, index):

        migrationsFolders = [folderName for folderName in os.listdir(self.__dirPath) if folderName.startswith("migrations")]

        if len(migrationsFolders) == 0:

            for folder in migrationFolderList:
                
                if not os.path.exists(folder):
                    os.mkdir(folder)
        
            self.renameFolder("migrations", migrationFolderList[index])

            print("Migration Folders Created")
    
    # endregion
    
    # region Rename Folder
   
    def renameFolder(self, newName, oldName):

        shutil.move(os.path.join(os.getcwd(), oldName), 
                  os.path.join(os.getcwd(), newName))
    
    # endregion
        
# endregion