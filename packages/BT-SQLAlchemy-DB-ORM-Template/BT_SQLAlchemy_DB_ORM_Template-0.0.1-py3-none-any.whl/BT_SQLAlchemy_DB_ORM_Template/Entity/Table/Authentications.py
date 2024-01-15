# region Import Packages

from Entity.ModelBase.ModelBase import *

# endregion

# region Authentication Table

class Authentications(BaseModel, db.Model):

    __tablename__ = "Authentications"

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.String(300), unique=True)
    Email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(300))
    Token = db.Column(db.String(300))
    ConfirmStatus = db.Column(db.Integer)
    CreatedBy = db.Column(db.String(300))
    CreatedAt = db.Column(db.String(30))
    ChangedBy = db.Column(db.String(300))
    ChangedAt = db.Column(db.String(30))
    Revision = db.Column(db.Integer)
    DeleteFlag = db.Column(db.Integer)

    def __init__(self, UserId, Email, Password, Token, ConfirmStatus, CreatedBy, CreatedAt, ChangedBy, ChangedAt, Revision, DeleteFlag):

        self.UserId = UserId
        self.Email = Email
        self.Password = Password
        self.Token = Token
        self.ConfirmStatus = ConfirmStatus
        self.CreatedBy = CreatedBy
        self.CreatedAt = CreatedAt
        self.ChangedBy = ChangedBy
        self.ChangedAt = ChangedAt
        self.Revision = Revision
        self.DeleteFlag = DeleteFlag

# endregion
