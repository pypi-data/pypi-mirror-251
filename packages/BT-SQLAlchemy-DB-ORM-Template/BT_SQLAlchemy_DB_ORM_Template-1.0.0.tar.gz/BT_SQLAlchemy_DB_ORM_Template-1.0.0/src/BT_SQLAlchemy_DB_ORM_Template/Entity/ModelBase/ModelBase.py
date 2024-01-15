#region Import Lib

from flask_sqlalchemy import SQLAlchemy
import datetime as dt

#endregion

#region Create Database

db = SQLAlchemy()

#endregion


#region BaseModels

class BaseModel(db.Model):

    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):

        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        
        return {
            column: value if not isinstance(value, dt.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

#endregion