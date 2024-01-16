# region Import Lib

from Entity.ModelBase.ModelBase import *

# endregion

# region AuthenticationLog Table

class AuthenticationLogs(BaseModel, db.Model):

    __tablename__ = "AuthenticationLogs"

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.String(300))
    Status = db.Column(db.String(10))
    ChangeStatusAt = db.Column(db.String(30))
    CreatedBy = db.Column(db.String(300))
    CreatedAt = db.Column(db.String(30))
    ChangedBy = db.Column(db.String(300))
    ChangedAt = db.Column(db.String(30))
    Revision = db.Column(db.Integer)
    DeleteFlag = db.Column(db.Integer)

    def __init__(self, UserId, Status, ChangeStatusAt, CreatedBy, CreatedAt, ChangedBy, ChangedAt, Revision, DeleteFlag):

        self.UserId = UserId
        self.Status = Status
        self.ChangeStatusAt = ChangeStatusAt
        self.CreatedBy = CreatedBy
        self.CreatedAt = CreatedAt
        self.ChangedBy = ChangedBy
        self.ChangedAt = ChangedAt
        self.Revision = Revision
        self.DeleteFlag = DeleteFlag

# endregion
