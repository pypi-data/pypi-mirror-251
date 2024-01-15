# region Import Packages

from flask import Flask

from Entity.Packages.EntityModels import *

from BlueWhale.MigrationFolderOS.MigrationFolderOS import MigrationFolderOS
from BlueWhale.Initializer.Initializer import Initializer
from BlueWhale.AppStart.AppStart import FlaskStart

from Entity.DbConfig.DbConfig import DbConfig
from Entity.Packages.EntityModels import *
from Entity.ModelBase.ModelBase import db

from Utils.GeneralLists import migrationFolderList

# endregion

# region Create Flask App

app = Flask(__name__)

# endregion

# region Flask App Variables

try:

    index = int(input("Enter the index of the database you want to connect to: "))

    if index < 0 or index > len(migrationFolderList) - 1:
        raise Exception("Invalid database index")
    
    Initializer().main(index)
    MigrationFolderOS().changeFolder(index)

except:

    raise Exception("You must enter a valid number")

DbConfigs = DbConfig(index)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DbConfig.dbUrl
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Enter your secret key here" 

#endregion

# region DB Create

db.init_app(app)

# endregion

# region Project Start

appOne = FlaskStart(app, __name__)

appOne.start()  

# endregion